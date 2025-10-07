
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"

def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class ReviseIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        new_status: Optional[str] = None,
        field_updates: Optional[Dict[str, Any]] = None,
        updated_by: str = ""
    ) -> str:
        incs = data.get("incidents", {})
        users = data.get("users", {})

        if not _ensure_exists(incs, incident_id):
            return json.dumps({"error": "incident_id not found"})
        if updated_by and not _ensure_exists(users, updated_by):
            return json.dumps({"error": "updated_by not found"})

        rec = incs[str(incident_id)].copy()
        if new_status:
            rec["status"] = new_status
        if field_updates:
            allowed = {
                "assigned_manager_id","component_id","severity","impact","urgency",
                "category","is_recurring","downtime_minutes","sla_breach","rto_breach"
            }
            for k, v in field_updates.items():
                if k in allowed:
                    rec[k] = v
        rec["updated_at"] = TS
        incs[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "revise_incident",
                "description": "Update incident fields and/or status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Incident ID (required)"},
                        "new_status": {"type": "string", "description": "Optional. Enum: open|in_progress|escalated|resolved|closed"},
                        "field_updates": {
                            "type": "object",
                            "description": "Optional. Allowed: assigned_manager_id|component_id|severity|impact|urgency|category|is_recurring|downtime_minutes|sla_breach|rto_breach"
                        },
                        "updated_by": {"type": "string", "description": "Optional. User id performing the update"}
                    },
                    # updated_by is OPTIONAL now
                    "required": ["incident_id"]
                }
            }
        }


