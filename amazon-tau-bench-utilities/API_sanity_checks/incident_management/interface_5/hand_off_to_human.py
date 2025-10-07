
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


class HandOffToHuman(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               reason_code: str,
               details: Optional[str] = None) -> str:
        if not reason_code:
            return json.dumps({"error":"reason_code is required"})
        return json.dumps({"success": True, "message": "Transferred to human", "reason_code": reason_code, "details": details})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"hand_off_to_human",
                "description":"Escalate the current request to a human operator when a halt condition is met.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "reason_code":{"type":"string","description":"Brief code (required)"},
                        "details":{"type":"string","description":"Short explanation (optional)"}
                    },
                    "required":["reason_code"]
                }
            }
        }
