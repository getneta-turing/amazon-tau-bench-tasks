
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
class LogIncidentCommunication(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        message_text: str,
        recipients_group: str,
        sent_by_user_id: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(sent_by_user_id) not in users:
            return json.dumps({"error": f"User {sent_by_user_id} not found"})

        allowed = ["end_users","stakeholders","executives","IT_staff"]
        if recipients_group not in allowed:
            return json.dumps({"error": f"Invalid recipients_group. Allowed: {allowed}"})

        comms = data.setdefault("communications", {})
        cid = _generate_id(comms)
        rec = {
            "communication_id": str(cid),
            "incident_id": str(incident_id),
            "recipients": recipients_group,
            "message_text": message_text,
            "sent_by_user_id": str(sent_by_user_id),
            "created_at": TIMESTAMP
        }
        comms[str(cid)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"log_incident_communication",
                "description":"Create a communication/status update record (no external sending).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "message_text":{"type":"string","description":"Message text"},
                        "recipients_group":{"type":"string","description":"Allowed: end_users, stakeholders, executives, IT_staff"},
                        "sent_by_user_id":{"type":"string","description":"User ID who sends the update"}
                    },
                    "required":["incident_id","message_text","recipients_group","sent_by_user_id"]
                }
            }
        }
