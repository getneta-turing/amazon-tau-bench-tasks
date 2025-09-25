############################################################
# 3) classify_severity.py
############################################################

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ClassifySeverity(Tool):
    """
    Assigns final incident severity based on provided evidence inputs (no inference).
    """

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        evidence_inputs: Dict[str, Any]
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})

        # Basic check: evidence_inputs must contain 'final_severity' and be in allowed range.
        sev = evidence_inputs.get("final_severity")
        allowed = ["P1", "P2", "P3", "P4"]
        if sev not in allowed:
            return json.dumps({"error": f"Invalid or missing final_severity in evidence_inputs. Allowed: {allowed}", "halt": True})

        inc = incidents[str(incident_id)]
        inc["severity"] = sev
        inc["updated_at"] = TS
        return json.dumps(inc)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "classify_severity",
                "description": "Set final incident severity using guided checks during creation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incident_id": {"type": "string", "description": "Incident ID to classify"},
                        "evidence_inputs": {"type": "object", "description": "Must include 'final_severity' with one of P1|P2|P3|P4"}
                    },
                    "required": ["incident_id", "evidence_inputs"]
                }
            }
        }
