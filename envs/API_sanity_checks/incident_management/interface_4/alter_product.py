
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


class AlterProduct(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               product_id: str,
               changes: Dict[str, Any]) -> str:
        products = data.get("products", {})
        if not _ensure_exists(products, product_id):
            return json.dumps({"error":"product_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"name","product_type","version","vendor_id","status"}
        rec = products[str(product_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        rec["updated_at"] = TS
        products[str(product_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"update_product",
                "description":"Modify product details.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "product_id":{"type":"string","description":"Product ID (required)"},
                        "changes":{"type":"object","description":"Allowed: name|product_type|version|vendor_id|status"}
                    },
                    "required":["product_id","changes"]
                }
            }
        }
