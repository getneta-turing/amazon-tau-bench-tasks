############################################################
# 13) schedule_pir.py
############################################################
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SchedulePIR(Tool):
    """
    Schedules a Post-Incident Review for a Closed incident.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        scheduled_date: str,
        facilitator_user_id: str
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        pirs = data.get("post_incident_reviews", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if str(facilitator_user_id) not in users:
            return json.dumps({"error": f"Facilitator {facilitator_user_id} not found", "halt": True})

        inc = incidents[str(incident_id)]
        if inc.get("status") != "closed":
            return json.dumps({"error": "Incident must be 'closed' before scheduling a PIR", "halt": True})

        pid = SchedulePIR._generate_id(pirs)
        rec = {
            "pir_id": pid,
            "incident_id": str(incident_id),
            "facilitator_user_id": str(facilitator_user_id),
            "scheduled_date": scheduled_date,  # (YYYY-MM-DD)
            "status": "scheduled",
            "completed_at": None,
            "created_at": TS
        }
        pirs[pid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"schedule_pir",
                "description":"Schedule a Post-Incident Review (PIR) for a CLOSED incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Closed incident ID (required)"},
                        "scheduled_date":{"type":"string","description":"Date (YYYY-MM-DD) when PIR is scheduled (required)"},
                        "facilitator_user_id":{"type":"string","description":"Facilitator user ID (required)"}
                    },
                    "required":["incident_id","scheduled_date","facilitator_user_id"]
                }
            }
        }
