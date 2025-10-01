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
class EscalateIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        escalated_to: str,
        reason_for_escalation: str,
        escalated_by_user_id: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(escalated_by_user_id) not in users:
            return json.dumps({"error": f"User {escalated_by_user_id} not found"})

        allowed = ["l2","l3","incident_manager","change_mgmt","facilities","devops"]
        if escalated_to not in allowed:
            return json.dumps({"error": "Invalid escalated_to. Allowed: L2, L3, incident_manager, change_mgmt, facilities, devops"})

        rec = incidents[str(incident_id)]
        rec["status"] = "escalated"
        incidents[str(incident_id)] = rec

        # record history
        hist = data.setdefault("incident_history", {})
        hid = _generate_id(hist)
        hist[str(hid)] = {
            "history_id": str(hid),
            "incident_id": str(incident_id),
            "changed_by_user_id": str(escalated_by_user_id),
            "field": "status",
            "old_value": None,
            "new_value": f"escalated_to:{escalated_to.lower()} reason:{reason_for_escalation}",
            "changed_at": TIMESTAMP
        }
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"escalate_incident",
                "description":"Escalate incident ownership and set status to escalated.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "escalated_to":{"type":"string","description":"Allowed: L2, L3, incident_manager, change_mgmt, facilities, devops"},
                        "reason_for_escalation":{"type":"string","description":"Reason for escalation"},
                        "escalated_by_user_id":{"type":"string","description":"User ID who escalates"}
                    },
                    "required":["incident_id","escalated_to","reason_for_escalation","escalated_by_user_id"]
                }
            }
        }
