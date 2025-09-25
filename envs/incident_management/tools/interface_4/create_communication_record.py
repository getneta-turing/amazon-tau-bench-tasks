############################################################
# 9) create_communication_record.py
############################################################
import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class CreateCommunicationRecord(Tool):
    """
    Records a stakeholder/customer/internal communication for an incident.
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
        sender_id: str,
        recipient_type: str,
        communication_type: str,
        delivery_method: str,
        message_summary: str,
        recipients: Optional[List[str]] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        comms = data.get("communications", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if str(sender_id) not in users:
            return json.dumps({"error": f"Sender {sender_id} not found", "halt": True})

        rt_allowed = ['stakeholders','customers','internal','specific_users']
        ct_allowed = ['incident_update','stakeholder_notice','customer_notice','internal_note']
        dm_allowed = ['email','sms','call','portal']

        if recipient_type not in rt_allowed:
            return json.dumps({"error": f"Invalid recipient_type. Allowed: {rt_allowed}", "halt": True})
        if communication_type not in ct_allowed:
            return json.dumps({"error": f"Invalid communication_type. Allowed: {ct_allowed}", "halt": True})
        if delivery_method not in dm_allowed:
            return json.dumps({"error": f"Invalid delivery_method. Allowed: {dm_allowed}", "halt": True})

        recipients_note = None
        if recipient_type == "specific_users":
            if not recipients or not isinstance(recipients, list):
                return json.dumps({"error": "For recipient_type specific_users, 'recipients' list is required", "halt": True})
            # Validate all user ids exist
            missing = [r for r in recipients if str(r) not in users]
            if missing:
                return json.dumps({"error": f"Recipients not found: {missing}", "halt": True})
            recipients_note = ",".join(str(r) for r in recipients)

        cid = CreateCommunicationRecord._generate_id(comms)
        rec = {
            "communication_id": cid,
            "incident_id": str(incident_id),
            "sender_id": str(sender_id),
            "recipient_type": recipient_type,
            "recipients_note": recipients_note,
            "communication_type": communication_type,
            "delivery_method": delivery_method,
            "delivery_status": "pending",
            "message_summary": message_summary,
            "sent_at": None,
            "created_at": TS
        }
        comms[cid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"record_communication",
                "description":"Record a communication associated with an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "sender_id":{"type":"string","description":"Sender user ID (required)"},
                        "recipient_type":{"type":"string","description":"Enum: stakeholders|customers|internal|specific_users (required)"},
                        "communication_type":{"type":"string","description":"Enum: incident_update|stakeholder_notice|customer_notice|internal_note (required)"},
                        "delivery_method":{"type":"string","description":"Enum: email|sms|call|portal (required)"},
                        "message_summary":{"type":"string","description":"Bounded summary (required)"},
                        "recipients":{"type":"array","items":{"type":"string"},"description":"List of user IDs when recipient_type is specific_users (optional)"}
                    },
                    "required":["incident_id","sender_id","recipient_type","communication_type","delivery_method","message_summary"]
                }
            }
        }
