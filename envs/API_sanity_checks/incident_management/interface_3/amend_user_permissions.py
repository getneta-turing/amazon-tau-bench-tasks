
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"



def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class AmendUserPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               user_id: str,
               requested_changes: Dict[str, Any],
               modified_by: str) -> str:
        users = data.get("users", {})

        if not _ensure_exists(users, user_id):
            return json.dumps({"error":"user_id not found"})
        if not _ensure_exists(users, modified_by):
            return json.dumps({"error":"modified_by not found"})
        if not requested_changes:
            return json.dumps({"error":"requested_changes is required"})

        allowed = {"role","status"}
        rec = users[str(user_id)].copy()
        for k,v in requested_changes.items():
            if k in allowed:
                rec[k] = v
        rec["updated_at"] = TS
        users[str(user_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"amend_user_permissions",
                "description":"Change user role or status.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "user_id":{"type":"string","description":"User ID (required)"},
                        "requested_changes":{"type":"object","description":"Allowed: role|status"},
                        "modified_by":{"type":"string","description":"User ID (required)"}
                    },
                    "required":["user_id","requested_changes","modified_by"]
                }
            }
        }
