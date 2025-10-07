
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"

def _generate_id(table: Dict[str, Any]) -> str:
    if not table:
        return "1"
    try:
        mx = max(int(k) for k in table.keys())
    except Exception:
        # fallback in case keys are not purely numeric strings
        nums = []
        for k in table.keys():
            try:
                nums.append(int(k))
            except:
                pass
        mx = max(nums) if nums else 0
    return str(mx + 1)

def _enum_ok(value: Optional[str], allowed: List[str]) -> bool:
    if value is None:
        return False
    return value in allowed

def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class RecordCommunicationEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               sender_user: str,
               recipient: str,
               delivery_method: str,
               message_content: str) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        comms = data.get("communications", {})

        allowed = ["email","phone_call","chat","incident_portal_update","automated_notification"]

        if not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if not _ensure_exists(users, sender_user):
            return json.dumps({"error":"sender_user not found"})
        if delivery_method not in allowed:
            return json.dumps({"error":"Invalid delivery_method. Allowed: email|phone_call|chat|incident_portal_update|automated_notification"})
        if not message_content:
            return json.dumps({"error":"message_content is required"})

        cid = _generate_id(comms)
        row = {
            "communication_id": cid,
            "incident_id": incident_id,
            "sender_id": sender_user,
            "recipient_type": "user",
            "recipient_user_id": recipient,
            "communication_type": delivery_method,
            "delivery_status": "pending",
            "subject": None,
            "message_body": message_content,
            "sent_at": TS,
            "created_at": TS
        }
        comms[cid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"record_communication",
                "description":"Log incident communications.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "sender_user":{"type":"string","description":"Sender user ID (required)"},
                        "recipient":{"type":"string","description":"User or group identifier (required)"},
                        "delivery_method":{"type":"string","description":"Required: email|phone_call|chat|incident_portal_update|automated_notification"},
                        "message_content":{"type":"string","description":"Message content (required)"}
                    },
                    "required":["incident_id","sender_user","recipient","delivery_method","message_content"]
                }
            }
        }
