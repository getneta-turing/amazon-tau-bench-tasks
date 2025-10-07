
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"

def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class SetIncidentResolved(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               resolved_by: str,
               resolution_summary: str) -> str:
        incs = data.get("incidents", {})
        users = data.get("users", {})
        if not _ensure_exists(incs, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if not _ensure_exists(users, resolved_by):
            return json.dumps({"error":"resolved_by not found"})
        if not resolution_summary:
            return json.dumps({"error":"resolution_summary is required"})

        rec = incs[str(incident_id)].copy()
        if rec.get("status") not in ("open","in_progress","escalated","resolved","closed"):
            pass
        rec["status"] = "resolved"
        rec["resolved_at"] = TS
        rec["updated_at"] = TS
        incs[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"set_incident_resolved",
                "description":"Mark incident as resolved; capture summary.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required; must be open|in_progress)"},
                        "resolved_by":{"type":"string","description":"User ID (required)"},
                        "resolution_summary":{"type":"string","description":"Summary (required)"}
                    },
                    "required":["incident_id","resolved_by","resolution_summary"]
                }
            }
        }
