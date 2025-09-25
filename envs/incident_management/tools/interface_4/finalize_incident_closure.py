############################################################
# 17) finalize_incident_closure.py
############################################################
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class FinalizeIncidentClosure(Tool):
    """
    Performs validations, sets Resolved, captures post-incident inputs, and sets Closed.
    """

    @staticmethod
    def _gen_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def _add_status_history(data: Dict[str, Any], incident_id: str, from_status: str, to_status: str, changer: str, reason: str = None):
        TS = "2025-10-01T00:00:00"
        hist = data.get("incident_status_history", {})
        hid = FinalizeIncidentClosure._gen_id(hist)
        hist[hid] = {
            "history_id": hid,
            "incident_id": str(incident_id),
            "from_status": from_status,
            "to_status": to_status,
            "reason": reason,
            "changed_by": str(changer),
            "changed_at": TS
        }
        data["incident_status_history"] = hist

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        validations_passed: bool,
        postmortem_title: str,
        clients_affected: List[str],
        detection_source: str,
        timeline_summary: str,
        severity: str,
        impact_summary: str,
        actions_taken: List[str],
        escalations_included: bool,
        communications_logged: bool,
        rca_started_or_prelim_root_cause: str,
        approval_reference: str = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        reports = data.get("reports", {})
        users = data.get("users", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})

        if not validations_passed:
            return json.dumps({"error": "Validations failed; cannot resolve and close incident", "halt": True})

        allowed_sev = ['P1','P2','P3','P4']
        if severity not in allowed_sev:
            return json.dumps({"error": f"Invalid severity for closure context. Allowed: {allowed_sev}", "halt": True})

        inc = incidents[str(incident_id)]
        prev_status = inc.get("status")

        # Step 1: move to resolved
        if prev_status not in ("resolved", "closed"):
            FinalizeIncidentClosure._add_status_history(data, incident_id, prev_status, "resolved", changer=inc.get("reporter_id"))
            inc["status"] = "resolved"
            inc["updated_at"] = TS

        # Create a postmortem report record
        rid = FinalizeIncidentClosure._gen_id(reports)
        reports[rid] = {
            "report_id": rid,
            "incident_id": str(incident_id),
            "generating_user_id": inc.get("reporter_id"),  # using reporter as generator by default
            "report_type": "postmortem",
            "status": "completed",
            "generated_at": TS,
            "created_at": TS
        }
        data["reports"] = reports

        # Step 2: move to closed
        if inc.get("status") != "closed":
            FinalizeIncidentClosure._add_status_history(data, incident_id, inc.get("status"), "closed", changer=inc.get("reporter_id"))
            inc["status"] = "closed"
            inc["updated_at"] = TS

        # Optionally incorporate some closure context in description (bounded)
        closure_bits = [
            f"ClientsAffected={len(clients_affected)}",
            f"Detection={detection_source}",
            f"SeverityFinal={severity}",
        ]
        inc["description"] = (inc.get("description") or "")[:800] + " [Closure: " + ";".join(closure_bits) + "]"

        return json.dumps(inc)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        sev_allowed = "P1|P2|P3|P4"
        return {
            "type":"function",
            "function":{
                "name":"resolve_and_close_incident",
                "description":"Resolve then close an incident after validations and capture of post-incident inputs.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "validations_passed":{"type":"boolean","description":"True/False (required)"},
                        "postmortem_title":{"type":"string","description":"Postmortem title (required)"},
                        "clients_affected":{"type":"array","items":{"type":"string"},"description":"List of client IDs (required)"},
                        "detection_source":{"type":"string","description":"Detection source (required)"},
                        "timeline_summary":{"type":"string","description":"Timeline summary (required)"},
                        "severity":{"type":"string","description":f"Enum: {sev_allowed} (required)"},
                        "impact_summary":{"type":"string","description":"Impact summary (required)"},
                        "actions_taken":{"type":"array","items":{"type":"string"},"description":"Actions taken (required)"},
                        "escalations_included":{"type":"boolean","description":"True/False (required)"},
                        "communications_logged":{"type":"boolean","description":"True/False (required)"},
                        "rca_started_or_prelim_root_cause":{"type":"string","description":"RCA started or preliminary root cause (required)"},
                        "approval_reference":{"type":"string","description":"Approval reference if required (optional)"}
                    },
                    "required":[
                        "incident_id","validations_passed","postmortem_title","clients_affected",
                        "detection_source","timeline_summary","severity","impact_summary",
                        "actions_taken","escalations_included","communications_logged","rca_started_or_prelim_root_cause"
                    ]
                }
            }
        }
