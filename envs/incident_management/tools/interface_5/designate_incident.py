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
class DesignateIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        assigned_team: str,
        responder_user_id: str,
        communication_message: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(responder_user_id) not in users:
            return json.dumps({"error": f"Responder user {responder_user_id} not found"})

        allowed = ["service_desk","l1","l2","l3","facilities","change_mgmt","devops","incident_manager","L1","L2","L3"]
        if assigned_team not in allowed:
            return json.dumps({"error": f"Invalid assigned_team. Allowed: service_desk,l1,l2,l3,facilities,change_mgmt,devops,incident_manager"})

        normalized_team = assigned_team.lower()

        # create assignment
        ia = data.setdefault("incident_assignments", {})
        aid = _generate_id(ia)
        ia[str(aid)] = {
            "assignment_id": str(aid),
            "incident_id": str(incident_id),
            "assigned_team": normalized_team,
            "responder_user_id": str(responder_user_id),
            "assigned_at": TIMESTAMP,
            "unassigned_at": None
        }

        # communication
        comms = data.setdefault("communications", {})
        cid = _generate_id(comms)
        comms[str(cid)] = {
            "communication_id": str(cid),
            "incident_id": str(incident_id),
            "recipients": "IT_staff",
            "message_text": communication_message,
            "sent_by_user_id": str(responder_user_id),
            "created_at": TIMESTAMP
        }

        # update incident
        rec = incidents[str(incident_id)]
        rec["status"] = "in_progress"
        incidents[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"designate_incident",
                "description":"Acknowledge and assign the incident to the correct tier; move to in_progress.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "assigned_team":{"type":"string","description":"Allowed: service_desk, L1, L2, L3, facilities, change_mgmt, devops"},
                        "responder_user_id":{"type":"string","description":"User ID of responder"},
                        "communication_message":{"type":"string","description":"Acknowledgement text stored in IMS"}
                    },
                    "required":["incident_id","assigned_team","responder_user_id","communication_message"]
                }
            }
        }
