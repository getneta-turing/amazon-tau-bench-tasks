
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


class RevisePostIncidentReview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               pir_id: str,
               changes: Dict[str, Any]) -> str:
        pirs = data.get("post_incident_reviews", {})
        if not _ensure_exists(pirs, pir_id):
            return json.dumps({"error":"pir_id not found"})
        if not changes:
            return json.dumps({"error":"changes is required"})

        allowed = {"scheduled_date","facilitator_user_id","timeline_accuracy_rating","communication_effectiveness_rating","technical_response_rating","status"}
        rec = pirs[str(pir_id)].copy()
        for k,v in changes.items():
            if k in allowed:
                rec[k] = v
        pirs[str(pir_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"revise_post_incident_review",
                "description":"Amend a PIR record.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "pir_id":{"type":"string","description":"PIR ID (required)"},
                        "changes":{"type":"object","description":"Allowed: scheduled_date|facilitator_user_id|timeline_accuracy_rating|communication_effectiveness_rating|technical_response_rating|status"}
                    },
                    "required":["pir_id","changes"]
                }
            }
        }
