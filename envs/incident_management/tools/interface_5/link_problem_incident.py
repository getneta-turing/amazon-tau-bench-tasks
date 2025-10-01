import json
from typing import Any, Dict
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



class LinkProblemIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        problem_id: str,
        incident_id: str,
        linked_by_user_id: str
    ) -> str:
        probs = data.get("problems", {})
        incs = data.get("incidents", {})
        users = data.get("users", {})
        if str(problem_id) not in probs:
            return json.dumps({"error": f"Problem {problem_id} not found"})
        if str(incident_id) not in incs:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(linked_by_user_id) not in users:
            return json.dumps({"error": f"User {linked_by_user_id} not found"})

        links = data.setdefault("problem_incident_links", {})
        lid = _generate_id(links)
        rec = {
            "link_id": str(lid),
            "problem_id": str(problem_id),
            "incident_id": str(incident_id),
            "linked_by_user_id": str(linked_by_user_id),
            "linked_at": TIMESTAMP
        }
        links[str(lid)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"link_problem_incident",
                "description":"Link an incident to a problem (bidirectional references).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "problem_id":{"type":"string","description":"Problem ID"},
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "linked_by_user_id":{"type":"string","description":"User ID who links"}
                    },
                    "required":["problem_id","incident_id","linked_by_user_id"]
                }
            }
        }
