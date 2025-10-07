
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


class RetrieveCommunications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               delivery_status: Optional[str] = None) -> str:
        comms = data.get("communications", {})
        out = []
        for r in comms.values():
            if r.get("incident_id") != incident_id:
                continue
            if delivery_status and r.get("delivery_status") != delivery_status:
                continue
            out.append(r)
        return json.dumps(out)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"retrieve_communications",
                "description":"List communications for an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "delivery_status":{"type":"string","description":"Optional: pending|sent|delivered|failed"}
                    },
                    "required":["incident_id"]
                }
            }
        }
