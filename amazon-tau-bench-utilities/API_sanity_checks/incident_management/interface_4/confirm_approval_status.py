
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


class ConfirmApprovalStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               reference_type: str,
               reference_id: str,
               requested_action: str,
               approver_id: str) -> str:
        approvals = data.get("approvals", {})
        users = data.get("users", {})
        if not _ensure_exists(users, approver_id):
            return json.dumps({"error":"approver_id not found"})

        status="pending"
        for ap in approvals.values():
            if ap.get("reference_type")==reference_type and ap.get("reference_id")==reference_id and ap.get("requested_action")==requested_action and ap.get("approver_id")==approver_id:
                status = ap.get("status","pending")
                break
        return json.dumps({"status": status})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"confirm_approval_status",
                "description":"Validate that required approval(s) exist for an action.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "reference_type":{"type":"string","description":"Target entity type (required)"},
                        "reference_id":{"type":"string","description":"Target entity id (required)"},
                        "requested_action":{"type":"string","description":"Required: create|update|resolve|close|escalate|publish|schedule|link|unlink"},
                        "approver_id":{"type":"string","description":"Approver user id (required)"}
                    },
                    "required":["reference_type","reference_id","requested_action","approver_id"]
                }
            }
        }
