############################################################
# 4) add_escalation.py
############################################################

import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddEscalation(Tool):
    """
    Records an escalation to a specific user or role.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        requester_id: str,
        target_user_id: Optional[str] = None,
        target_role: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        escalations = data.get("escalations", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if str(requester_id) not in users:
            return json.dumps({"error": f"Requester {requester_id} not found", "halt": True})

        allowed_roles = ['incident_manager','resolver','communications_lead','change_authority','compliance_audit','service_desk','requester']
        if target_role is not None and target_role not in allowed_roles:
            return json.dumps({"error": f"Invalid target_role. Allowed: {allowed_roles}", "halt": True})

        if target_user_id is not None and str(target_user_id) not in users:
            return json.dumps({"error": f"Target user {target_user_id} not found", "halt": True})

        esc_id = AddEscalation._generate_id(escalations)
        rec = {
            "escalation_id": esc_id,
            "incident_id": str(incident_id),
            "target_user_id": str(target_user_id) if target_user_id is not None else None,
            "target_role": target_role,
            "status": "requested",
            "created_by": str(requester_id),
            "created_at": TS,
            "updated_at": TS
        }
        escalations[esc_id] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        allowed_roles = "incident_manager|resolver|communications_lead|change_authority|compliance_audit|service_desk|requester"
        return {
            "type":"function",
            "function":{
                "name":"create_escalation",
                "description":"Record an escalation to a user or role for an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "requester_id":{"type":"string","description":"User ID of the requester (required)"},
                        "target_user_id":{"type":"string","description":"Target user ID (optional)"},
                        "target_role":{"type":"string","description":f"Target role enum: {allowed_roles} (optional)"}
                    },
                    "required":["incident_id","requester_id"]
                }
            }
        }
