
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


class ModifyComponent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               component_id: str,
               changes: Dict[str, Any]) -> str:
        components = data.get("components", {})
        if not _ensure_exists(components, component_id):
            return json.dumps({"error":"component_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"name","component_type","environment","location","ports","status"}
        rec = components[str(component_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                if k == "ports":
                    rec["port_number"] = v
                else:
                    rec[k] = v
        rec["updated_at"] = TS
        components[str(component_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"modify_component",
                "description":"Modify component details.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "component_id":{"type":"string","description":"Component ID (required)"},
                        "changes":{"type":"object","description":"Allowed: name|component_type|environment|location|ports|status"}
                    },
                    "required":["component_id","changes"]
                }
            }
        }
