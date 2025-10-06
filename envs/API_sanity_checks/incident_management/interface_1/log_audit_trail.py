
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


class LogAuditTrail(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               action: str,
               reference_type: str,
               reference_id: str,
               field_name: Optional[str] = None,
               old_value: Optional[str] = None,
               new_value: Optional[str] = None) -> str:
        users = data.get("users", {})
        audits = data.get("audit_trails", {})
        allowed_actions = ["identify","create","update","escalate","notify","resolve","close","review","kb_update","vendor_engagement","simulation","tool_use"]

        if not _ensure_exists(users, user_id):
            return json.dumps({"error":"user_id not found"})
        if action not in allowed_actions:
            return json.dumps({"error":"Invalid action"})

        aid = _generate_id(audits)
        row = {
            "audit_id": aid,
            "reference_type": reference_type,
            "reference_id": reference_id,
            "action": action,
            "user_id": user_id,
            "field_name": field_name,
            "old_value": old_value,
            "new_value": new_value,
            "created_at": TS
        }
        audits[aid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"log_audit_trail",
                "description":"Write required audit records.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "user_id":{"type":"string","description":"User ID (required)"},
                        "action":{"type":"string","description":"Required: identify|create|update|escalate|notify|resolve|close|review|kb_update|vendor_engagement|simulation|tool_use"},
                        "reference_type":{"type":"string","description":"Reference type (required)"},
                        "reference_id":{"type":"string","description":"Reference id (required)"},
                        "field_name":{"type":"string","description":"Optional field name"},
                        "old_value":{"type":"string","description":"Optional old value"},
                        "new_value":{"type":"string","description":"Optional new value"}
                    },
                    "required":["user_id","action","reference_type","reference_id"]
                }
            }
        }
