
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


class ProposeChangeRequest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               change_title: str,
               change_type: str,
               risk_level: str,
               requested_by: str,
               incident_id: Optional[str] = None) -> str:
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        changes = data.get("change_requests", {})
        ctypes = ["standard","emergency","normal"]
        risks = ["low","medium","high","critical"]

        if not change_title or not change_type or not risk_level or not requested_by:
            return json.dumps({"error":"change_title, change_type, risk_level, requested_by are required"})
        if change_type not in ctypes:
            return json.dumps({"error":"Invalid change_type. Allowed: standard|emergency|normal"})
        if risk_level not in risks:
            return json.dumps({"error":"Invalid risk_level. Allowed: low|medium|high|critical"})
        if not _ensure_exists(users, requested_by):
            return json.dumps({"error":"requested_by not found"})
        if incident_id is not None and not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})

        cid = _generate_id(changes)
        row = {
            "change_id": cid,
            "incident_id": incident_id,
            "title": change_title,
            "change_type": change_type,
            "risk_level": risk_level,
            "requested_by_id": requested_by,
            "approved_by_id": None,
            "status": "requested",
            "scheduled_start": None,
            "scheduled_end": None,
            "actual_start": None,
            "actual_end": None,
            "created_at": TS
        }
        changes[cid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"propose_change_request",
                "description":"Propose a change linked to an incident (optional).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "change_title":{"type":"string","description":"Title (required)"},
                        "change_type":{"type":"string","description":"Required: standard|emergency|normal"},
                        "risk_level":{"type":"string","description":"Required: low|medium|high|critical"},
                        "requested_by":{"type":"string","description":"Requester user id (required)"},
                        "incident_id":{"type":"string","description":"Optional incident id"}
                    },
                    "required":["change_title","change_type","risk_level","requested_by"]
                }
            }
        }
