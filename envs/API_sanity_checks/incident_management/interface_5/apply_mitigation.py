
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


class ApplyMitigation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               description: str,
               effectiveness: str,
               implemented_by: str) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        workarounds = data.get("workarounds", {})

        allowed = ["effective","partially_effective","ineffective"]

        if not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if not _ensure_exists(users, implemented_by):
            return json.dumps({"error":"implemented_by not found"})
        if effectiveness not in allowed:
            return json.dumps({"error":"Invalid effectiveness. Allowed: effective|partially_effective|ineffective"})
        if not description:
            return json.dumps({"error":"description is required"})

        wid = _generate_id(workarounds)
        row = {
            "workaround_id": wid,
            "incident_id": incident_id,
            "implemented_by_id": implemented_by,
            "effectiveness": effectiveness,
            "status": "active",
            "description": description,
            "implemented_at": TS
        }
        workarounds[wid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"implement_workaround",
                "description":"Capture temporary mitigation.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "description":{"type":"string","description":"Description (required)"},
                        "effectiveness":{"type":"string","description":"Required: effective|partially_effective|ineffective"},
                        "implemented_by":{"type":"string","description":"User ID (required)"}
                    },
                    "required":["incident_id","description","effectiveness","implemented_by"]
                }
            }
        }
