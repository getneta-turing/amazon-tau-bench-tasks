############################################################
# 16) set_incident_status.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SetIncidentStatus(Tool):
    """
    Transitions an incident to a target status with stamping and status history recording.
    """

    @staticmethod
    def _generate_hist_id(hist: Dict[str, Any]) -> str:
        if not hist:
            return "1"
        return str(max(int(k) for k in hist.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        target_status: str,
        requester_id: str,
        reason: Optional[str] = None,
        approval_reference: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        hist = data.get("incident_status_history", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if str(requester_id) not in users:
            return json.dumps({"error": f"Requester {requester_id} not found", "halt": True})

        allowed_status = ['new','triage','in_progress','mitigated','resolved','closed','cancelled']
        if target_status not in allowed_status:
            return json.dumps({"error": f"Invalid target_status. Allowed: {allowed_status}", "halt": True})

        inc = incidents[str(incident_id)]
        prev = inc.get("status")

        # Simple transition guard: cannot go from closed/cancelled back to active
        if prev in ("closed", "cancelled") and target_status not in ("closed","cancelled"):
            return json.dumps({"error": f"Cannot transition from {prev} to {target_status}", "halt": True})

        inc["status"] = target_status
        inc["updated_at"] = TS

        hid = SetIncidentStatus._generate_hist_id(hist)
        hist[hid] = {
            "history_id": hid,
            "incident_id": str(incident_id),
            "from_status": prev,
            "to_status": target_status,
            "reason": reason,
            "changed_by": str(requester_id),
            "changed_at": TS
        }
        data["incident_status_history"] = hist

        return json.dumps(inc)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        allowed_status = "new|triage|in_progress|mitigated|resolved|closed|cancelled"
        return {
            "type":"function",
            "function":{
                "name":"update_incident_status",
                "description":"Update an incident's status with validation and status history logging.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "target_status":{"type":"string","description":f"Enum: {allowed_status} (required)"},
                        "requester_id":{"type":"string","description":"User ID performing the update (required)"},
                        "reason":{"type":"string","description":"Optional reason for status change"},
                        "approval_reference":{"type":"string","description":"Approval reference if required (optional)"}
                    },
                    "required":["incident_id","target_status","requester_id"]
                }
            }
        }
