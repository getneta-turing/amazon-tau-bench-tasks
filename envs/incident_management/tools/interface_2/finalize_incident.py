import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool



TIMESTAMP = "2025-10-01T00:00:00"
class FinalizeIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        closed_by_user_id: str,
        closure_notes: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(closed_by_user_id) not in users:
            return json.dumps({"error": f"User {closed_by_user_id} not found"})

        rec = incidents[str(incident_id)]
        if rec.get("status") != "resolved":
            return json.dumps({"error": "Incident must be in resolved status before closing"})

        rec["status"] = "closed"
        rec["closed_by_user_id"] = str(closed_by_user_id)
        rec["closed_at"] = TIMESTAMP
        rec["closure_notes"] = closure_notes
        incidents[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"finalize_incident",
                "description":"Close an incident after verification.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "closed_by_user_id":{"type":"string","description":"User ID who closes the incident"},
                        "closure_notes":{"type":"string","description":"Closure notes"}
                    },
                    "required":["incident_id","closed_by_user_id","closure_notes"]
                }
            }
        }
