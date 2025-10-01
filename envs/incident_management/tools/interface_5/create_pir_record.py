import json
from typing import Any, Dict
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
class CreatePIRRecord(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        review_notes: str,
        conducted_by_user_id: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(conducted_by_user_id) not in users:
            return json.dumps({"error": f"User {conducted_by_user_id} not found"})

        pir = data.setdefault("post_incident_reviews", {})
        rid = _generate_id(pir)
        rec = {
            "review_id": str(rid),
            "incident_id": str(incident_id),
            "conducted_by_user_id": str(conducted_by_user_id),
            "notes": review_notes,
            "created_at": TIMESTAMP
        }
        pir[str(rid)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_pir_record",
                "description":"Create a post-incident review record for a high-priority incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "review_notes":{"type":"string","description":"Review notes"},
                        "conducted_by_user_id":{"type":"string","description":"User ID who conducted the review (Incident Manager)"}
                    },
                    "required":["incident_id","review_notes","conducted_by_user_id"]
                }
            }
        }
