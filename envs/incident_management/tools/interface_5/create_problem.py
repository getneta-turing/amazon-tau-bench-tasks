import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

def _generate_id(table: Dict[str, Any]) -> str:
    if not table:
        return "1"
    try:
        return str(max(int(k) for k in table.keys()) + 1)
    except Exception:
        # Fallback in case keys are not numeric strings
        return str(len(table) + 1)

TIMESTAMP = "2025-10-01T00:00:00"

class CreateProblem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        problem_title: str,
        description: str,
        detection_source: str,
        created_by_user_id: str,
        related_incident_ids: Optional[List[str]] = None
    ) -> str:
        users = data.get("users", {})
        if str(created_by_user_id) not in users:
            return json.dumps({"error": f"User {created_by_user_id} not found"})
        allowed = ["user_report","monitoring_tool","automated_alert"]
        if detection_source not in allowed:
            return json.dumps({"error": f"Invalid detection_source. Allowed: {allowed}"})
        probs = data.setdefault("problems", {})
        pid = _generate_id(probs)
        rec = {
            "problem_id": str(pid),
            "title": problem_title,
            "description": description,
            "detection_source": detection_source,
            "status": "open",
            "known_error": False,
            "created_by_user_id": str(created_by_user_id),
            "resolved_by_user_id": None,
            "closed_by_user_id": None,
            "created_at": TIMESTAMP,
            "resolved_at": None,
            "closed_at": None
        }
        probs[str(pid)] = rec

        if related_incident_ids:
            links = data.setdefault("problem_incident_links", {})
            incidents = data.get("incidents", {})
            for iid in related_incident_ids:
                if str(iid) in incidents:
                    lid = _generate_id(links)
                    links[str(lid)] = {
                        "link_id": str(lid),
                        "problem_id": str(pid),
                        "incident_id": str(iid),
                        "linked_by_user_id": str(created_by_user_id),
                        "linked_at": TIMESTAMP
                    }
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_problem",
                "description":"Create a problem (underlying cause) and optionally link incidents.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "problem_title":{"type":"string","description":"Problem title"},
                        "description":{"type":"string","description":"Problem description"},
                        "detection_source":{"type":"string","description":"Allowed: user_report, monitoring_tool, automated_alert"},
                        "created_by_user_id":{"type":"string","description":"User ID who creates the problem"},
                        "related_incident_ids":{"type":"array","items":{"type":"string"},"description":"Optional list of incident IDs to link"}
                    },
                    "required":["problem_title","description","detection_source","created_by_user_id"]
                }
            }
        }
