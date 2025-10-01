import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


TIMESTAMP = "2025-10-01T00:00:00"
# 5) prioritize_incident
class AssignIncidentPriority(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, priority: str, justification: str) -> str:
        allowed = ["low","medium","high"]
        if priority not in allowed:
            return json.dumps({"error": f"Invalid priority. Allowed: {allowed}"})
        incidents = data.get("incidents", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        rec = incidents[str(incident_id)]
        rec["priority"] = priority
        rec["priority_justification"] = justification
        incidents[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"assign_incident_priority",
                "description":"Set incident priority with justification.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "priority":{"type":"string","description":"Allowed: low, medium, high"},
                        "justification":{"type":"string","description":"Reason for priority"}
                    },
                    "required":["incident_id","priority","justification"]
                }
            }
        }
