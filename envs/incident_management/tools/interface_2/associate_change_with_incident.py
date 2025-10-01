
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

def _generate_id(table: Dict[str, Any]) -> str:
    if not table:
        return "1"
    try:
        return str(max(int(k) for k in table.keys()) + 1)
    except Exception:
        # Fallback in case keys are not numeric strings
        return str(len(table) + 1)

TIMESTAMP = "2025-10-01T00:00:00"
class AssociateChangeToIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        change_summary: str,
        requested_by: str,
        approval_record_id: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        approvals = data.get("approvals", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(requested_by) not in users:
            return json.dumps({"error": f"User {requested_by} not found"})
        if str(approval_record_id) not in approvals or approvals[str(approval_record_id)].get("status") != "approved":
            return json.dumps({"error": f"Approval {approval_record_id} not found or not approved"})

        cr = data.setdefault("change_requests", {})
        cid = _generate_id(cr)
        cr[str(cid)] = {
            "change_id": str(cid),
            "incident_id": str(incident_id),
            "requested_by_user_id": str(requested_by),
            "summary": change_summary,
            "approval_status": "approved",
            "approved_by_user_id": approvals[str(approval_record_id)].get("approved_by_user_id"),
            "approved_at": TIMESTAMP,
            "implemented_at": None,
            "created_at": TIMESTAMP
        }
        return json.dumps(cr[str(cid)])

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"Associate_change_to_incident",
                "description":"Record the change coordination reference and approvals related to the incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "change_summary":{"type":"string","description":"Summary of the required change"},
                        "requested_by":{"type":"string","description":"User ID requesting the change"},
                        "approval_record_id":{"type":"string","description":"Existing approval record ID that is approved"}
                    },
                    "required":["incident_id","change_summary","requested_by","approval_record_id"]
                }
            }
        }
