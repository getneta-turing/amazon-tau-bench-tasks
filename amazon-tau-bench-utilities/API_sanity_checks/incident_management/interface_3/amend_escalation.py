
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"

def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class AmendEscalation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               escalation_id: str,
               changes: Dict[str, Any]) -> str:
        escs = data.get("escalations", {})
        if not _ensure_exists(escs, escalation_id):
            return json.dumps({"error":"escalation_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"acknowledged_at","resolved_at","status"}
        rec = escs[str(escalation_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        escs[str(escalation_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"amend_escalation",
                "description":"Modify escalation timestamps/status.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "escalation_id":{"type":"string","description":"Escalation ID (required)"},
                        "changes":{"type":"object","description":"Allowed: acknowledged_at|resolved_at|status"}
                    },
                    "required":["escalation_id","changes"]
                }
            }
        }
