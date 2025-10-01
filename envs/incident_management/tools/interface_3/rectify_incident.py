import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"
class RectifyIncident(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        resolution_summary: str,
        resolved_by_user_id: str,
        resolution_timestamp: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(resolved_by_user_id) not in users:
            return json.dumps({"error": f"User {resolved_by_user_id} not found"})

        rec = incidents[str(incident_id)]
        rec["status"] = "resolved"
        rec["resolved_by_user_id"] = str(resolved_by_user_id)
        rec["resolved_at"] = resolution_timestamp
        rec["resolution_summary"] = resolution_summary
        incidents[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"rectify_incident",
                "description":"Record permanent fix and set status to resolved.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "resolution_summary":{"type":"string","description":"Summary of resolution"},
                        "resolved_by_user_id":{"type":"string","description":"User ID who resolved"},
                        "resolution_timestamp":{"type":"string","description":"Timestamp of resolution (YYYY-MM-DD)"}
                    },
                    "required":["incident_id","resolution_summary","resolved_by_user_id","resolution_timestamp"]
                }
            }
        }
