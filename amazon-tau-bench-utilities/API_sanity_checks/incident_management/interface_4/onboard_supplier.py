
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


class OnboardSupplier(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               vendor_name: str,
               contact_email: str,
               contact_phone: str,
               vendor_type: str) -> str:
        vendors = data.get("vendors", {})
        allowed = ["hardware_provider","software_provider","cloud_service_provider","consulting_partner"]

        if not vendor_name or not contact_email or not contact_phone or not vendor_type:
            return json.dumps({"error":"vendor_name, contact_email, contact_phone, vendor_type are required"})

        if vendor_type not in allowed:
            return json.dumps({"error":"Invalid vendor_type. Allowed: hardware_provider|software_provider|cloud_service_provider|consulting_partner"})

        vendor_id = _generate_id(vendors)
        row = {
            "vendor_id": vendor_id,
            "name": vendor_name,
            "vendor_type": vendor_type,
            "contact_email": contact_email,
            "contact_phone": contact_phone,
            "status": "active",
            "created_at": TS,
            "updated_at": TS
        }
        vendors[vendor_id] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"onboard_supplier",
                "description":"Onboard a vendor/third party.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "vendor_name":{"type":"string","description":"Vendor name (required)"},
                        "contact_email":{"type":"string","description":"Vendor email (required)"},
                        "contact_phone":{"type":"string","description":"Vendor phone (required)"},
                        "vendor_type":{"type":"string","description":"Required: hardware_provider|software_provider|cloud_service_provider|consulting_partner"}
                    },
                    "required":["vendor_name","contact_email","contact_phone","vendor_type"]
                }
            }
        }
