
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


class RequestRollback(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               change_id: str,
               justification: str,
               requested_by: str,
               incident_id: Optional[str] = None) -> str:
        changes = data.get("change_requests", {})
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        rollbacks = data.get("rollback_requests", {})

        if not _ensure_exists(changes, change_id):
            return json.dumps({"error":"change_id not found"})
        if not justification:
            return json.dumps({"error":"justification is required"})
        if not _ensure_exists(users, requested_by):
            return json.dumps({"error":"requested_by not found"})
        if incident_id is not None and not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})

        rid = _generate_id(rollbacks)
        row = {
            "rollback_id": rid,
            "change_id": change_id,
            "incident_id": incident_id,
            "requested_by_id": requested_by,
            "approved_by_id": None,
            "status": "requested",
            "executed_at": None,
            "justification": justification,
            "validation_completed": False,
            "created_at": TS
        }
        rollbacks[rid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"request_rollback",
                "description":"Request rollback of a change.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "change_id":{"type":"string","description":"Change ID (required)"},
                        "justification":{"type":"string","description":"Justification (required)"},
                        "requested_by":{"type":"string","description":"Requester user id (required)"},
                        "incident_id":{"type":"string","description":"Optional incident id"}
                    },
                    "required":["change_id","justification","requested_by"]
                }
            }
        }
