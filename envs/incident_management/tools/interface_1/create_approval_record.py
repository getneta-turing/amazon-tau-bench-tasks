############################################################
# 14) create_approval_record.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateApprovalRecord(Tool):
    """
    Records an approval/decision for a scoped action.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        approval_reference: str,
        action_scope: str,
        target_entity_type: str,
        target_entity_id: str,
        approver_user_id: str,
        approver_role: str,
        decision: str,
        note: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        approvals = data.get("approvals", {})
        users = data.get("users", {})

        if str(approver_user_id) not in users:
            return json.dumps({"error": f"Approver {approver_user_id} not found", "halt": True})

        scope_allowed = ['incident_creation','severity_set','status_transition','escalation','workaround','rca','change_request','rollback','communication','resolution','closure','report_generation','kb_publish','pir_schedule']
        type_allowed = ['incident','problem','change_request','work_order','communication','rca','workaround','report','knowledge','pir']
        role_allowed = ['incident_manager','change_authority','communications_lead','compliance_audit']
        decision_allowed = ['approved','rejected']

        if action_scope not in scope_allowed:
            return json.dumps({"error": f"Invalid action_scope. Allowed: {scope_allowed}", "halt": True})
        if target_entity_type not in type_allowed:
            return json.dumps({"error": f"Invalid target_entity_type. Allowed: {type_allowed}", "halt": True})
        if approver_role not in role_allowed:
            return json.dumps({"error": f"Invalid approver_role. Allowed: {role_allowed}", "halt": True})
        if decision not in decision_allowed:
            return json.dumps({"error": f"Invalid decision. Allowed: {decision_allowed}", "halt": True})

        aid = CreateApprovalRecord._generate_id(approvals)
        rec = {
            "approval_id": aid,
            "approval_reference": approval_reference,
            "action_scope": action_scope,
            "target_entity_type": target_entity_type,
            "target_entity_id": str(target_entity_id),
            "approver_user_id": str(approver_user_id),
            "approver_role": approver_role,
            "decision": decision,
            "decided_at": TS,
            "note": note
        }
        approvals[aid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        scope_allowed = "incident_creation|severity_set|status_transition|escalation|workaround|rca|change_request|rollback|communication|resolution|closure|report_generation|kb_publish|pir_schedule"
        type_allowed = "incident|problem|change_request|work_order|communication|rca|workaround|report|knowledge|pir"
        role_allowed = "incident_manager|change_authority|communications_lead|compliance_audit"
        decision_allowed = "approved|rejected"
        return {
            "type":"function",
            "function":{
                "name":"create_approval_record",
                "description":"Record an approval/decision for a scoped action in IMS.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "approval_reference":{"type":"string","description":"Approval reference string (required)"},
                        "action_scope":{"type":"string","description":f"Enum: {scope_allowed} (required)"},
                        "target_entity_type":{"type":"string","description":f"Enum: {type_allowed} (required)"},
                        "target_entity_id":{"type":"string","description":"Target entity ID (required)"},
                        "approver_user_id":{"type":"string","description":"Approver user ID (required)"},
                        "approver_role":{"type":"string","description":f"Enum: {role_allowed} (required)"},
                        "decision":{"type":"string","description":f"Enum: {decision_allowed} (required)"},
                        "note":{"type":"string","description":"Optional note"}
                    },
                    "required":["approval_reference","action_scope","target_entity_type","target_entity_id","approver_user_id","approver_role","decision"]
                }
            }
        }
