
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


class AlterRollbackRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               rollback_id: str,
               changes: Dict[str, Any]) -> str:
        rbs = data.get("rollback_requests", {})
        if not _ensure_exists(rbs, rollback_id):
            return json.dumps({"error":"rollback_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"approved_by_id","executed_at","validation_completed","status"}
        rec = rbs[str(rollback_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        rbs[str(rollback_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"alter_rollback_request",
                "description":"Advance rollback lifecycle.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "rollback_id":{"type":"string","description":"Rollback ID (required)"},
                        "changes":{"type":"object","description":"Allowed: approved_by_id|executed_at|validation_completed|status"}
                    },
                    "required":["rollback_id","changes"]
                }
            }
        }
