############################################################
# 2) register_incident.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class RegisterIncident(Tool):
    """
    Creates an incident after validation, duplicate check, and optional approval reference.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reporter_id: str,
        client_id: str,
        title: str,
        description: str,
        category: str,
        severity_candidate: str,
        impact: str,
        component_id: Optional[str] = None,
        approval_reference: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        # Validate foreign keys and enums
        users = data.get("users", {})
        clients = data.get("clients", {})
        components = data.get("components", {})
        incidents = data.get("incidents", {})

        if str(reporter_id) not in users:
            return json.dumps({"error": f"Reporter {reporter_id} not found", "halt": True})
        if str(client_id) not in clients:
            return json.dumps({"error": f"Client {client_id} not found", "halt": True})
        if component_id is not None and str(component_id) not in components:
            return json.dumps({"error": f"Component {component_id} not found", "halt": True})

        allowed_category = ['infrastructure','application','network','security','service_request','other']
        if category not in allowed_category:
            return json.dumps({"error": f"Invalid category. Allowed: {allowed_category}", "halt": True})

        allowed_sev = ['P1','P2','P3','P4']
        if severity_candidate not in allowed_sev:
            return json.dumps({"error": f"Invalid severity_candidate. Allowed: {allowed_sev}", "halt": True})

        # Duplicate open incident check (same client + title & not closed/cancelled)
        for inc in incidents.values():
            if inc.get("client_id") == client_id and inc.get("title") == title and inc.get("status") not in ("closed","cancelled","resolved"):
                return json.dumps({"error": "Duplicate active incident detected for the same client and title", "halt": True})

        new_id = RegisterIncident._generate_id(incidents)

        # Concise way to preserve "impact" without schema change: append to description
        desc = description
        if impact:
            desc = f"{description} [Impact: {impact}]"

        record = {
            "incident_id": str(new_id),
            "reporter_id": str(reporter_id),
            "client_id": str(client_id),
            "component_id": str(component_id) if component_id is not None else None,
            "title": title,
            "description": desc,
            "category": category,
            "severity": severity_candidate,  # initial severity as candidate
            "status": "new",
            "detection_ts": TS,
            "created_at": TS,
            "updated_at": TS
        }
        incidents[str(new_id)] = record

        # Also create initial status history row
        hist = data.get("incident_status_history", {})
        def _gen_hist_id():
            if not hist:
                return "1"
            return str(max(int(k) for k in hist.keys()) + 1)
        hid = _gen_hist_id()
        hist[hid] = {
            "history_id": hid,
            "incident_id": str(new_id),
            "from_status": None,
            "to_status": "new",
            "reason": "incident_created",
            "changed_by": str(reporter_id),
            "changed_at": TS
        }
        data["incident_status_history"] = hist

        return json.dumps(record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        allowed_category = "infrastructure|application|network|security|service_request|other"
        allowed_sev = "P1|P2|P3|P4"
        return {
            "type": "function",
            "function": {
                "name": "create_incident",
                "description": "Create a new incident after validation and duplication check.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reporter_id": {"type": "string", "description": "ID of reporting user"},
                        "client_id": {"type": "string", "description": "ID of the client"},
                        "title": {"type": "string", "description": "Incident title"},
                        "description": {"type": "string", "description": "Incident description (bounded)"},
                        "category": {"type": "string", "description": f"Category enum: {allowed_category}"},
                        "severity_candidate": {"type": "string", "description": f"Severity enum: {allowed_sev}"},
                        "impact": {"type": "string", "description": "Impact summary (bounded)"},
                        "component_id": {"type": "string", "description": "Component ID (optional)"},
                        "approval_reference": {"type": "string", "description": "Approval reference if required (optional)"}
                    },
                    "required": ["reporter_id","client_id","title","description","category","severity_candidate","impact"]
                }
            }
        }
