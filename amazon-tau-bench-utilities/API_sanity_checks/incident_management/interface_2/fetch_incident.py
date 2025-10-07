
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


class FetchIncident(Tool):
    @staticmethod
    def _match(rec: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        for k, v in (filters or {}).items():
            rv = rec.get(k)
            if k in ("detected_at_from","detected_at_to"):
                continue
            if v is None:
                continue
            if isinstance(v, str):
                if rv is None or str(rv).lower() != v.lower():
                    return False
            else:
                if rv != v:
                    return False
        return True

    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: Optional[str] = None,
               filters: Optional[Dict[str, Any]] = None) -> str:
        incs = data.get("incidents", {})
        out = []
        if incident_id:
            rec = incs.get(str(incident_id))
            return json.dumps([rec] if rec else [])
        for rec in incs.values():
            if FetchIncident._match(rec, filters or {}):
                out.append(rec)
        return json.dumps(out)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"fetch_incident",
                "description":"Retrieve one incident or a filtered list.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Optional incident id"},
                        "filters":{"type":"object","description":"Optional filters: client_id|status|severity|category|detected_at_from|detected_at_to"}
                    },
                    "required":[]
                }
            }
        }
