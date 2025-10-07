
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


class ReviseClient(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               client_id: str,
               changes: Dict[str, Any],
               requester_id: str) -> str:
        clients = data.get("clients", {})
        users   = data.get("users", {})

        if not _ensure_exists(clients, client_id):
            return json.dumps({"error":"client_id not found"})
        if not _ensure_exists(users, requester_id):
            return json.dumps({"error":"requester_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"name","registration_number","contact_email","client_type","contact_phone","address","status"}
        rec = clients[str(client_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        rec["updated_at"] = TS
        clients[str(client_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"revise_client",
                "description":"Modify client fields.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "client_id":{"type":"string","description":"Client ID (required)"},
                        "changes":{"type":"object","description":"Allowed: name|registration_number|contact_email|client_type|contact_phone|address|status (at least one)"},
                        "requester_id":{"type":"string","description":"User ID (required)"}
                    },
                    "required":["client_id","changes","requester_id"]
                }
            }
        }
