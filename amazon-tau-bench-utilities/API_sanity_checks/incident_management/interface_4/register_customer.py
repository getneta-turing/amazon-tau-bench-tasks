
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


class RegisterCustomer(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               name: str,
               registration_number: str,
               contact_email: str,
               client_type: str,
               contact_phone: Optional[str] = None,
               address: Optional[str] = None) -> str:
        clients = data.get("clients", {})
        allowed_types = ["enterprise","mid_market","small_business","startup"]

        if not name or not registration_number or not contact_email or not client_type:
            return json.dumps({"error":"name, registration_number, contact_email, client_type are required"})

        if client_type not in allowed_types:
            return json.dumps({"error":"Invalid client_type. Allowed: enterprise|mid_market|small_business|startup"})

        client_id = _generate_id(clients)
        row = {
            "client_id": client_id,
            "name": name,
            "registration_number": registration_number,
            "contact_email": contact_email,
            "client_type": client_type,
            "status": "active",
            "contact_phone": contact_phone,
            "address": address,
            "created_at": TS,
            "updated_at": TS
        }
        clients[client_id] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_client",
                "description":"Register a new client.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "name":{"type":"string","description":"Client name (required)"},
                        "registration_number":{"type":"string","description":"Registration number (required)"},
                        "contact_email":{"type":"string","description":"Contact email (required)"},
                        "client_type":{"type":"string","description":"Required: enterprise|mid_market|small_business|startup"},
                        "contact_phone":{"type":"string","description":"Optional phone"},
                        "address":{"type":"string","description":"Optional address"}
                    },
                    "required":["name","registration_number","contact_email","client_type"]
                }
            }
        }
