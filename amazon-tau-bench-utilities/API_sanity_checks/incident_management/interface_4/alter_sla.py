
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


class AlterSla(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               sla_id: str,
               changes: Dict[str, Any]) -> str:
        sla = data.get("sla_agreements", {})
        if not _ensure_exists(sla, sla_id):
            return json.dumps({"error":"sla_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"response_time_minutes","resolution_time_hours","availability_target","status","severity_level"}
        rec = sla[str(sla_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        rec["created_at"] = rec.get("created_at") or TS
        sla[str(sla_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"alter_sla",
                "description":"Update an SLA row.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "sla_id":{"type":"string","description":"SLA ID (required)"},
                        "changes":{"type":"object","description":"Allowed: response_time_minutes|resolution_time_hours|availability_target|status|severity_level"}
                    },
                    "required":["sla_id","changes"]
                }
            }
        }
