############################################################
# 11) generate_incident_report.py
############################################################
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GenerateIncidentReport(Tool):
    """
    Generates a report from incident and related records.
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
        report_type: str,
        generating_user_id: str
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        reports = data.get("reports", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if str(generating_user_id) not in users:
            return json.dumps({"error": f"User {generating_user_id} not found", "halt": True})

        allowed = ['summary','timeline','postmortem','metrics']
        if report_type not in allowed:
            return json.dumps({"error": f"Invalid report_type. Allowed: {allowed}", "halt": True})

        rid = GenerateIncidentReport._generate_id(reports)
        rec = {
            "report_id": rid,
            "incident_id": str(incident_id),
            "generating_user_id": str(generating_user_id),
            "report_type": report_type,
            "status": "completed",
            "generated_at": TS,
            "created_at": TS
        }
        reports[rid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"generate_incident_report",
                "description":"Generate an incident report of a given type.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "report_type":{"type":"string","description":"Enum: summary|timeline|postmortem|metrics (required)"},
                        "generating_user_id":{"type":"string","description":"User ID generating the report (required)"}
                    },
                    "required":["incident_id","report_type","generating_user_id"]
                }
            }
        }
