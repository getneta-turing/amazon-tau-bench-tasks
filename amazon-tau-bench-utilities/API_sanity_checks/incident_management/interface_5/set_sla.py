
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


class SetSla(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               subscription_id: str,
               severity_level: str,
               response_time_minutes: int,
               resolution_time_hours: int,
               availability_target: Optional[float] = None) -> str:
        subs = data.get("subscriptions", {})
        sla  = data.get("sla_agreements", {})
        allowed_sev = ["P1","P2","P3","P4"]

        if not _ensure_exists(subs, subscription_id):
            return json.dumps({"error":"subscription_id not found"})
        if severity_level not in allowed_sev:
            return json.dumps({"error":"Invalid severity_level. Allowed: P1|P2|P3|P4"})
        if response_time_minutes is None or resolution_time_hours is None:
            return json.dumps({"error":"response_time_minutes and resolution_time_hours are required"})

        sid = _generate_id(sla)
        row = {
            "sla_id": sid,
            "subscription_id": subscription_id,
            "severity_level": severity_level,
            "response_time_minutes": int(response_time_minutes),
            "resolution_time_hours": int(resolution_time_hours),
            "availability_target": availability_target,
            "status": "active",
            "created_at": TS
        }
        sla[sid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"set_sla",
                "description":"Define SLA per severity for a subscription.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "subscription_id":{"type":"string","description":"Subscription ID (required)"},
                        "severity_level":{"type":"string","description":"Required: P1|P2|P3|P4"},
                        "response_time_minutes":{"type":"integer","description":"Response time in minutes (required)"},
                        "resolution_time_hours":{"type":"integer","description":"Resolution time in hours (required)"},
                        "availability_target":{"type":"number","description":"Optional availability target (e.g., 99.9)"}
                    },
                    "required":["subscription_id","severity_level","response_time_minutes","resolution_time_hours"]
                }
            }
        }
