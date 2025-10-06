
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


class SchedulePostIncidentReview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               scheduled_date: str,
               facilitator_user_id: str) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        pirs = data.get("post_incident_reviews", {})

        if not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if not scheduled_date:
            return json.dumps({"error":"scheduled_date (YYYY-MM-DD) is required"})
        if not _ensure_exists(users, facilitator_user_id):
            return json.dumps({"error":"facilitator_user_id not found"})

        pid = _generate_id(pirs)
        row = {
            "pir_id": pid,
            "incident_id": incident_id,
            "scheduled_date": scheduled_date,
            "facilitator_user_id": facilitator_user_id,
            "status": "scheduled",
            "timeline_accuracy_rating": None,
            "communication_effectiveness_rating": None,
            "technical_response_rating": None,
            "created_at": TS
        }
        pirs[pid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"schedule_post_incident_review",
                "description":"Schedule a post-incident review (PIR).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "scheduled_date":{"type":"string","description":"Date (YYYY-MM-DD) (required)"},
                        "facilitator_user_id":{"type":"string","description":"User ID (required)"}
                    },
                    "required":["incident_id","scheduled_date","facilitator_user_id"]
                }
            }
        }
