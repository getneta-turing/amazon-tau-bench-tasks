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
class CaptureIncidentDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        incident_description: str,
        timestamp: str,
        affected_service: Optional[str] = None,
        initial_diagnosis: Optional[str] = None,
        workaround_note: Optional[str] = None
    ) -> str:
        incidents = data.get("incidents", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        rec = incidents[str(incident_id)]

        if affected_service:
            services = data.get("services", {})
            if str(affected_service) not in services:
                return json.dumps({"error": f"Service {affected_service} not found"})
            rec["affected_service_id"] = str(affected_service)

        # Update core fields
        rec["initial_description"] = incident_description
        # Optional: capture diagnosis/workaround as history entries
        history = data.setdefault("incident_history", {})
        if initial_diagnosis:
            hid = _generate_id(history)
            history[str(hid)] = {
                "history_id": str(hid),
                "incident_id": str(incident_id),
                "changed_by_user_id": rec.get("reporter_id"),
                "field": "other",
                "old_value": None,
                "new_value": f"diagnosis: {initial_diagnosis}",
                "changed_at": timestamp
            }
        if workaround_note:
            wid = _generate_id(history)
            history[str(wid)] = {
                "history_id": str(wid),
                "incident_id": str(incident_id),
                "changed_by_user_id": rec.get("reporter_id"),
                "field": "workaround",
                "old_value": None,
                "new_value": workaround_note,
                "changed_at": timestamp
            }

        incidents[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"log_incident_details",
                "description":"Capture/append core details (description, impact, affected service) to an existing incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"ID of the incident to update"},
                        "incident_description":{"type":"string","description":"Updated/extended description of the incident"},
                        "affected_service":{"type":"string","description":"Service ID (services.service_id) to mark as affected"},
                        "timestamp":{"type":"string","description":"Timestamp in ISO format (YYYY-MM-DD) or full ISO"},
                        "initial_diagnosis":{"type":"string","description":"Optional initial diagnosis text"},
                        "workaround_note":{"type":"string","description":"Optional workaround note"}
                    },
                    "required":["incident_id","incident_description","timestamp"]
                }
            }
        }
