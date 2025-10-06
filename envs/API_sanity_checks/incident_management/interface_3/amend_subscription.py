
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"



def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class AmendSubscription(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               subscription_id: str,
               changes: Dict[str, Any]) -> str:
        subs = data.get("subscriptions", {})
        if not _ensure_exists(subs, subscription_id):
            return json.dumps({"error":"subscription_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"subscription_type","service_level_tier","start_date","end_date","rto_hours","status"}
        rec = subs[str(subscription_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        rec["updated_at"] = TS
        subs[str(subscription_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"amend_subscription",
                "description":"Modify a client subscription.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "subscription_id":{"type":"string","description":"Subscription ID (required)"},
                        "changes":{"type":"object","description":"Allowed: subscription_type|service_level_tier|start_date|end_date|rto_hours|status"}
                    },
                    "required":["subscription_id","changes"]
                }
            }
        }
