import json
from typing import Any, Dict, Optional, List
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

class DocumentDiagnosisWorkaround(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        diagnostic_steps_summary: str,
        workaround_applied: bool,
        responder_user_id: str,
        workaround_details: Optional[str] = None
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(responder_user_id) not in users:
            return json.dumps({"error": f"User {responder_user_id} not found"})

        # history note
        hist = data.setdefault("incident_history", {})
        hid = _generate_id(hist)
        hist[str(hid)] = {
            "history_id": str(hid),
            "incident_id": str(incident_id),
            "changed_by_user_id": str(responder_user_id),
            "field": "other",
            "old_value": None,
            "new_value": f"diagnosis: {diagnostic_steps_summary}",
            "changed_at": TIMESTAMP
        }

        # workaround if applied
        if workaround_applied:
            iwa = data.setdefault("incident_workarounds", {})
            wid = _generate_id(iwa)
            iwa[str(wid)] = {
                "incident_workaround_id": str(wid),
                "incident_id": str(incident_id),
                "summary": workaround_details or "Workaround applied",
                "applied_by_user_id": str(responder_user_id),
                "applied_at": TIMESTAMP,
                "active": True
            }

        return json.dumps(incidents[str(incident_id)])

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"document_diagnosis_workaround",
                "description":"Record diagnostic steps and optionally a temporary workaround.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "diagnostic_steps_summary":{"type":"string","description":"Summary of diagnostic steps"},
                        "workaround_applied":{"type":"boolean","description":"Whether a workaround was applied (True/False)"},
                        "responder_user_id":{"type":"string","description":"User ID who recorded diagnosis"},
                        "workaround_details":{"type":"string","description":"Optional workaround details"}
                    },
                    "required":["incident_id","diagnostic_steps_summary","workaround_applied","responder_user_id"]
                }
            }
        }
