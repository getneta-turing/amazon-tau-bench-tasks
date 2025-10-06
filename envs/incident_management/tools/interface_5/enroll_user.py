
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


class EnrollUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               name: str,
               email: str,
               role: str,
               timezone: str,
               department: Optional[str] = None,
               client_id: Optional[str] = None,
               vendor_id: Optional[str] = None) -> str:
        users = data.get("users", {})
        clients = data.get("clients", {})
        vendors = data.get("vendors", {})

        allowed_roles = ["incident_manager","technical_support","account_manager","executive","vendor_contact","system_administrator","client_contact"]

        if not name or not email or not role or not timezone:
            return json.dumps({"error":"name, email, role, timezone are required"})

        if role not in allowed_roles:
            return json.dumps({"error":"Invalid role. Allowed: incident_manager|technical_support|account_manager|executive|vendor_contact|system_administrator|client_contact"})

        if client_id is not None and not _ensure_exists(clients, client_id):
            return json.dumps({"error":"client_id not found"})
        if vendor_id is not None and not _ensure_exists(vendors, vendor_id):
            return json.dumps({"error":"vendor_id not found"})

        # Split name into first/last naive
        parts = name.strip().split()
        first = parts[0]
        last  = parts[-1] if len(parts)>1 else ""

        user_id = _generate_id(users)
        row = {
            "user_id": user_id,
            "first_name": first,
            "last_name": last,
            "email": email,
            "role": role,
            "timezone": timezone,
            "status": "active",
            "client_id": client_id,
            "vendor_id": vendor_id,
            "created_at": TS,
            "updated_at": TS
        }
        users[user_id] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_user",
                "description":"Add a user with role/associations.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "name":{"type":"string","description":"Full name (required)"},
                        "email":{"type":"string","description":"Email (required)"},
                        "role":{"type":"string","description":"Required: incident_manager|technical_support|account_manager|executive|vendor_contact|system_administrator|client_contact"},
                        "timezone":{"type":"string","description":"IANA timezone (required)"},
                        "department":{"type":"string","description":"Optional free-text department"},
                        "client_id":{"type":"string","description":"Optional client association"},
                        "vendor_id":{"type":"string","description":"Optional vendor association"}
                    },
                    "required":["name","email","role","timezone"]
                }
            }
        }
