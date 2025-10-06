
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


class RegisterProduct(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               product_name: str,
               product_type: str,
               version: Optional[str] = None,
               vendor_id: Optional[str] = None) -> str:
        products = data.get("products", {})
        vendors  = data.get("vendors", {})
        allowed_types = ["payment_processing","banking_system","api_gateway","data_integration","reporting_platform","security_service","backup_service","monitoring_tool","other"]

        if not product_name or not product_type:
            return json.dumps({"error":"product_name and product_type are required"})

        if product_type not in allowed_types:
            return json.dumps({"error":"Invalid product_type. Allowed: payment_processing|banking_system|api_gateway|data_integration|reporting_platform|security_service|backup_service|monitoring_tool|other"})

        if vendor_id is not None and not _ensure_exists(vendors, vendor_id):
            return json.dumps({"error":"vendor_id not found"})

        product_id = _generate_id(products)
        row = {
            "product_id": product_id,
            "name": product_name,
            "product_type": product_type,
            "version": version,
            "vendor_id": vendor_id,
            "status": "active",
            "created_at": TS,
            "updated_at": TS
        }
        products[product_id] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"register_product",
                "description":"Track a supported system/app.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "product_name":{"type":"string","description":"Product name (required)"},
                        "product_type":{"type":"string","description":"Required: payment_processing|banking_system|api_gateway|data_integration|reporting_platform|security_service|backup_service|monitoring_tool|other"},
                        "version":{"type":"string","description":"Optional version"},
                        "vendor_id":{"type":"string","description":"Optional vendor link"}
                    },
                    "required":["product_name","product_type"]
                }
            }
        }
