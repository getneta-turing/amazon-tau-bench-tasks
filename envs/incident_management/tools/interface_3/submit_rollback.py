############################################################
# 8) submit_rollbackt.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SubmitRollback(Tool):
    """
    Files a rollback request against an existing change.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        change_id: str,
        requester_id: str,
        rollback_justification: str,
        scope: str,
        incident_id: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        changes = data.get("change_requests", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        rollbacks = data.get("rollback_requests", {})

        if str(change_id) not in changes:
            return json.dumps({"error": f"Change {change_id} not found", "halt": True})
        if str(requester_id) not in users:
            return json.dumps({"error": f"Requester {requester_id} not found", "halt": True})
        if incident_id is not None and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})

        allowed_scope = ['partial','full']
        if scope not in allowed_scope:
            return json.dumps({"error": f"Invalid scope. Allowed: {allowed_scope}", "halt": True})

        rid = SubmitRollback._generate_id(rollbacks)
        rec = {
            "rollback_id": rid,
            "change_id": str(change_id),
            "incident_id": str(incident_id) if incident_id is not None else None,
            "requester_id": str(requester_id),
            "justification": rollback_justification,
            "scope": scope,
            "status": "requested",
            "requested_at": TS,
            "updated_at": TS
        }
        rollbacks[rid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_rollback_request",
                "description":"File a rollback request against a change request.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "change_id":{"type":"string","description":"Target change_id (required)"},
                        "requester_id":{"type":"string","description":"Requester user ID (required)"},
                        "rollback_justification":{"type":"string","description":"Bounded justification (required)"},
                        "scope":{"type":"string","description":"Enum: partial|full (required)"},
                        "incident_id":{"type":"string","description":"Optional incident_id to associate (optional)"}
                    },
                    "required":["change_id","requester_id","rollback_justification","scope"]
                }
            }
        }
