
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


class ProvisionSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               client_id: str,
               product_id: str,
               subscription_type: str,
               service_level_tier: str,
               start_date: str,
               end_date: Optional[str] = None,
               recovery_objectives: Optional[str] = None) -> str:
        clients = data.get("clients", {})
        products = data.get("products", {})
        subscriptions = data.get("subscriptions", {})

        allowed_types = ["full_service","limited_service","trial","custom"]
        allowed_tier  = ["premium","standard","basic"]

        if not _ensure_exists(clients, client_id):
            return json.dumps({"error":"client_id not found"})
        if not _ensure_exists(products, product_id):
            return json.dumps({"error":"product_id not found"})

        if subscription_type not in allowed_types:
            return json.dumps({"error":"Invalid subscription_type. Allowed: full_service|limited_service|trial|custom"})
        if service_level_tier not in allowed_tier:
            return json.dumps({"error":"Invalid service_level_tier. Allowed: premium|standard|basic"})
        if not start_date:
            return json.dumps({"error":"start_date (YYYY-MM-DD) is required"})

        sid = _generate_id(subscriptions)
        row = {
            "subscription_id": sid,
            "client_id": client_id,
            "product_id": product_id,
            "subscription_type": subscription_type,
            "service_level_tier": service_level_tier,
            "rto_hours": None,
            "start_date": start_date,
            "end_date": end_date,
            "status": "active",
            "created_at": TS,
            "updated_at": TS
        }
        subscriptions[sid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_subscription",
                "description":"Establish client coverage for a product.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "client_id":{"type":"string","description":"Client ID (required)"},
                        "product_id":{"type":"string","description":"Product ID (required)"},
                        "subscription_type":{"type":"string","description":"Required: full_service|limited_service|trial|custom"},
                        "service_level_tier":{"type":"string","description":"Required: premium|standard|basic"},
                        "start_date":{"type":"string","description":"Start date (YYYY-MM-DD) (required)"},
                        "end_date":{"type":"string","description":"Optional end date (YYYY-MM-DD)"},
                        "recovery_objectives":{"type":"string","description":"Optional RTO text"}
                    },
                    "required":["client_id","product_id","subscription_type","service_level_tier","start_date"]
                }
            }
        }
