############################################################
# 6) start_rca.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class StartRCA(Tool):
    """
    Starts a Root Cause Analysis for an incident.
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
        conducting_user_id: str,
        analysis_method: str,
        timeline_summary: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        rcas = data.get("root_cause_analyses", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if str(conducting_user_id) not in users:
            return json.dumps({"error": f"User {conducting_user_id} not found", "halt": True})

        allowed_methods = ['five_whys','fishbone','timeline','fault_tree','postmortem']
        if analysis_method not in allowed_methods:
            return json.dumps({"error": f"Invalid analysis_method. Allowed: {allowed_methods}", "halt": True})

        rid = StartRCA._generate_id(rcas)
        rec = {
            "rca_id": rid,
            "incident_id": str(incident_id),
            "conducting_user_id": str(conducting_user_id),
            "analysis_method": analysis_method,
            "timeline_summary": timeline_summary,
            "status": "in_progress",
            "created_at": TS,
            "updated_at": TS
        }
        rcas[rid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        allowed_methods = "five_whys|fishbone|timeline|fault_tree|postmortem"
        return {
            "type":"function",
            "function":{
                "name":"start_rca",
                "description":"Start a Root Cause Analysis (RCA) for an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "conducting_user_id":{"type":"string","description":"User ID conducting RCA (required)"},
                        "analysis_method":{"type":"string","description":f"Analysis method enum: {allowed_methods} (required)"},
                        "timeline_summary":{"type":"string","description":"Concise optional summary"}
                    },
                    "required":["incident_id","conducting_user_id","analysis_method"]
                }
            }
        }
