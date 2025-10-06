
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


class AlterChangeRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               change_id: str,
               changes: Dict[str, Any]) -> str:
        chg = data.get("change_requests", {})
        if not _ensure_exists(chg, change_id):
            return json.dumps({"error":"change_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"title","change_type","approved_by_id","risk_level","scheduled_start","scheduled_end","actual_start","actual_end","status"}
        rec = chg[str(change_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        chg[str(change_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"update_change_request",
                "description":"Adjust details or advance status of a change.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "change_id":{"type":"string","description":"Change ID (required)"},
                        "changes":{"type":"object","description":"Allowed: title|change_type|approved_by_id|risk_level|scheduled_start|scheduled_end|actual_start|actual_end|status"}
                    },
                    "required":["change_id","changes"]
                }
            }
        }
