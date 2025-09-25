############################################################
# 18) abort_change_or_rollback.py
############################################################
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AbortChangeOrRollback(Tool):
    """
    Cancels a change request or a rollback request when permitted.
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        target_type: str,
        target_id: str,
        requester_id: str,
        reason: str,
        approval_reference: str = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        users = data.get("users", {})
        if str(requester_id) not in users:
            return json.dumps({"error": f"Requester {requester_id} not found", "halt": True})

        if target_type == "change_request":
            changes = data.get("change_requests", {})
            if str(target_id) not in changes:
                return json.dumps({"error": f"Change request {target_id} not found", "halt": True})
            cr = changes[str(target_id)]
            if cr.get("status") in ("cancelled","failed","implemented","rolled_back"):
                return json.dumps({"error": f"Cannot cancel change in status {cr.get('status')}", "halt": True})
            prev = cr.get("status")
            cr["status"] = "cancelled"
            cr["updated_at"] = TS
            return json.dumps(cr)

        elif target_type == "rollback":
            rbs = data.get("rollback_requests", {})
            if str(target_id) not in rbs:
                return json.dumps({"error": f"Rollback request {target_id} not found", "halt": True})
            rb = rbs[str(target_id)]
            if rb.get("status") in ("cancelled","executed","failed"):
                return json.dumps({"error": f"Cannot cancel rollback in status {rb.get('status')}", "halt": True})
            prev = rb.get("status")
            rb["status"] = "cancelled"
            rb["updated_at"] = TS
            return json.dumps(rb)

        else:
            return json.dumps({"error": "Invalid target_type. Allowed: change_request|rollback", "halt": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"cancel_change_or_rollback",
                "description":"Cancel a change request or a rollback request if allowed.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "target_type":{"type":"string","description":"Enum: change_request|rollback (required)"},
                        "target_id":{"type":"string","description":"change_id or rollback_id (required)"},
                        "requester_id":{"type":"string","description":"Requester user ID (required)"},
                        "reason":{"type":"string","description":"Reason for cancellation (required)"},
                        "approval_reference":{"type":"string","description":"Approval reference if required (optional)"}
                    },
                    "required":["target_type","target_id","requester_id","reason"]
                }
            }
        }
