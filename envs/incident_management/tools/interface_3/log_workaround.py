############################################################
# 5) log_workaround.py
############################################################

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LogWorkaround(Tool):
    """
    Logs an active workaround linked to an incident.
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
        implementing_user_id: str,
        workaround_description: str,
        effectiveness: str
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        workarounds = data.get("workarounds", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if str(implementing_user_id) not in users:
            return json.dumps({"error": f"User {implementing_user_id} not found", "halt": True})

        allowed_eff = ['ineffective','partial','effective']
        if effectiveness not in allowed_eff:
            return json.dumps({"error": f"Invalid effectiveness. Allowed: {allowed_eff}", "halt": True})

        wid = LogWorkaround._generate_id(workarounds)
        rec = {
            "workaround_id": wid,
            "incident_id": str(incident_id),
            "implementing_user_id": str(implementing_user_id),
            "description": workaround_description,
            "effectiveness": effectiveness,
            "status": "active",
            "created_at": TS,
            "updated_at": TS
        }
        workarounds[wid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_workaround",
                "description":"Create an active workaround for an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "implementing_user_id":{"type":"string","description":"User ID who implements the workaround (required)"},
                        "workaround_description":{"type":"string","description":"Bounded description of the workaround (required)"},
                        "effectiveness":{"type":"string","description":"Effectiveness enum: ineffective|partial|effective (required)"}
                    },
                    "required":["incident_id","implementing_user_id","workaround_description","effectiveness"]
                }
            }
        }
