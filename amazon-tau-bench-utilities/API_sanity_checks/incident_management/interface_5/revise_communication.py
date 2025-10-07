
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


class ReviseCommunication(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               communication_id: str,
               changes: Dict[str, Any]) -> str:
        comms = data.get("communications", {})
        if not _ensure_exists(comms, communication_id):
            return json.dumps({"error":"communication_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"recipient","recipient_user_id","delivery_method","message_content","delivery_status","sent_at"}
        rec = comms[str(communication_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                if k=="delivery_method":
                    rec["communication_type"] = v
                elif k=="message_content":
                    rec["message_body"] = v
                else:
                    rec[k] = v
        comms[str(communication_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"update_communication",
                "description":"Adjust a communication record (while pending).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "communication_id":{"type":"string","description":"Communication ID (required)"},
                        "changes":{"type":"object","description":"Allowed: recipient|recipient_user_id|delivery_method|message_content|delivery_status|sent_at"}
                    },
                    "required":["communication_id","changes"]
                }
            }
        }
