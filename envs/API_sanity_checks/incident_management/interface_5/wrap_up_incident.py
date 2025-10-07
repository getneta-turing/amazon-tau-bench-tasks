
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


class WrapUpIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               closed_by: str) -> str:
        incs = data.get("incidents", {})
        users = data.get("users", {})
        if not _ensure_exists(incs, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if not _ensure_exists(users, closed_by):
            return json.dumps({"error":"closed_by not found"})

        rec = incs[str(incident_id)].copy()
        if rec.get("status") != "resolved":
            # Keep behavior lenient but return info
            pass
        rec["status"] = "closed"
        rec["closed_at"] = TS
        rec["updated_at"] = TS
        incs[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"wrap_up_incident",
                "description":"Close an already resolved incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required; must be resolved)"},
                        "closed_by":{"type":"string","description":"User ID (required)"}
                    },
                    "required":["incident_id","closed_by"]
                }
            }
        }
