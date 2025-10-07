
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


class TriggerEscalation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               target_user: str,
               reason: str,
               requested_by: str,
               escalation_level: str) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        escalations = data.get("escalations", {})
        reasons = ["sla_breach","severity_increase","resource_unavailable","executive_request","client_demand"]
        levels = ["technical","management","executive","vendor"]

        if not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if not _ensure_exists(users, target_user):
            return json.dumps({"error":"target_user not found"})
        if not _ensure_exists(users, requested_by):
            return json.dumps({"error":"requested_by not found"})
        if reason not in reasons:
            return json.dumps({"error":"Invalid reason. Allowed: " + "|".join(reasons)})
        if escalation_level not in levels:
            return json.dumps({"error":"Invalid escalation_level. Allowed: " + "|".join(levels)})

        eid = _generate_id(escalations)
        row = {
            "escalation_id": eid,
            "incident_id": incident_id,
            "escalated_by_id": requested_by,
            "escalated_to_id": target_user,
            "escalation_reason": reason,
            "escalation_level": escalation_level,
            "status": "open",
            "escalated_at": TS,
            "acknowledged_at": None,
            "resolved_at": None
        }
        escalations[eid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"trigger_escalation",
                "description":"Escalate an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "target_user":{"type":"string","description":"Escalation target user ID (required)"},
                        "reason":{"type":"string","description":"Required: sla_breach|severity_increase|resource_unavailable|executive_request|client_demand"},
                        "requested_by":{"type":"string","description":"Requester user ID (required)"},
                        "escalation_level":{"type":"string","description":"Required: technical|management|executive|vendor"}
                    },
                    "required":["incident_id","target_user","reason","requested_by","escalation_level"]
                }
            }
        }
