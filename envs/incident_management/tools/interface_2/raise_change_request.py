############################################################
# 7) raise_change_request.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RaiseChangeRequest(Tool):
    """
    Creates a change request optionally linked to an incident.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        title: str,
        change_type: str,
        risk: str,
        incident_id: Optional[str] = None,
        approval_reference: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        changes = data.get("change_requests", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"Requester {requester_id} not found", "halt": True})
        if incident_id is not None and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})

        allowed_types = ['standard','normal','emergency']
        allowed_risk = ['low','medium','high']
        if change_type not in allowed_types:
            return json.dumps({"error": f"Invalid change_type. Allowed: {allowed_types}", "halt": True})
        if risk not in allowed_risk:
            return json.dumps({"error": f"Invalid risk. Allowed: {allowed_risk}", "halt": True})

        cid = RaiseChangeRequest._generate_id(changes)
        rec = {
            "change_id": cid,
            "requested_by": str(requester_id),
            "incident_id": str(incident_id) if incident_id is not None else None,
            "title": title,
            "change_type": change_type,
            "risk": risk,
            "status": "requested",
            "requested_at": TS,
            "updated_at": TS
        }
        changes[cid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        allowed_types = "standard|normal|emergency"
        allowed_risk = "low|medium|high"
        return {
            "type":"function",
            "function":{
                "name":"create_change_request",
                "description":"Create a change request optionally linked to an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester (required)"},
                        "title":{"type":"string","description":"Change request title (required)"},
                        "change_type":{"type":"string","description":f"Enum: {allowed_types} (required)"},
                        "risk":{"type":"string","description":f"Enum: {allowed_risk} (required)"},
                        "incident_id":{"type":"string","description":"Incident ID (optional)"},
                        "approval_reference":{"type":"string","description":"Approval reference if required (optional)"}
                    },
                    "required":["requester_id","title","change_type","risk"]
                }
            }
        }
