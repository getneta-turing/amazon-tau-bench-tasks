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
class FileIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reporter_id: str, detection_source: str, initial_description: str) -> str:
        users = data.get("users", {})
        if str(reporter_id) not in users:
            return json.dumps({"error": f"Reporter {reporter_id} not found"})

        allowed_sources = ["user_report", "monitoring_tool", "automated_alert"]
        if detection_source not in allowed_sources:
            return json.dumps({"error": f"Invalid detection_source. Allowed: {allowed_sources}"})

        incidents = data.setdefault("incidents", {})
        new_id = _generate_id(incidents)
        rec = {
            "incident_id": str(new_id),
            "reporter_id": str(reporter_id),
            "detection_source": detection_source,
            "category": "other",
            "priority": "medium",
            "severity": "medium",
            "status": "open",
            "affected_service_id": None,
            "initial_description": initial_description,
            "source_event_id": None,
            "created_at": TIMESTAMP,
            "resolved_at": None,
            "closed_at": None,
            "resolved_by_user_id": None,
            "closed_by_user_id": None
        }
        incidents[str(new_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"file_incident",
                "description":"Incident identification; start a new incident in open status.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "reporter_id":{"type":"string","description":"ID of the reporter (user in users table)"},
                        "detection_source":{"type":"string","description":"Detection source enum allowed: user_report, monitoring_tool, automated_alert"},
                        "initial_description":{"type":"string","description":"Initial description of the incident"}
                    },
                    "required":["reporter_id","detection_source","initial_description"]
                }
            }
        }
