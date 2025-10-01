import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


TIMESTAMP = "2025-10-01T00:00:00"
class LabelIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, category: str, sub_category: Optional[str] = None) -> str:
        allowed = ["hardware","software","security","performance","other"]
        if category not in allowed:
            return json.dumps({"error": f"Invalid category. Allowed: {allowed}"})
        incidents = data.get("incidents", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        rec = incidents[str(incident_id)]
        rec["category"] = category
        if sub_category is not None:
            # store as extra attribute (not enforced by schema, but harmless for JSON storage)
            rec["sub_category"] = sub_category
        incidents[str(incident_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"label_incident",
                "description":"Set incident category (and optional subcategory).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "category":{"type":"string","description":"Allowed: hardware, software, security, performance, other"},
                        "sub_category":{"type":"string","description":"Optional free-form subcategory"}
                    },
                    "required":["incident_id","category"]
                }
            }
        }
