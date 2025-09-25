############################################################
# 15) create_audit_log.py
############################################################
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateAuditLog(Tool):
    """
    Writes a bounded audit entry capturing actor, reference, action, and summary.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        actor_user_id: str,
        reference_type: str,
        reference_id: str,
        action: str,
        summary: str
    ) -> str:
        TS = "2025-10-01T00:00:00"
        audits = data.get("audit_trails", {})
        users = data.get("users", {})

        if str(actor_user_id) not in users:
            return json.dumps({"error": f"Actor {actor_user_id} not found", "halt": True})

        ref_allowed = ['user','client','component','incident','problem','change_request','work_order','escalation','workaround','rca','communication','status_history','report','metric','knowledge','pir','approval']
        act_allowed = ['create','read','update','delete','approve','reject','status_change','link','generate']

        if reference_type not in ref_allowed:
            return json.dumps({"error": f"Invalid reference_type. Allowed: {ref_allowed}", "halt": True})
        if action not in act_allowed:
            return json.dumps({"error": f"Invalid action. Allowed: {act_allowed}", "halt": True})

        aid = CreateAuditLog._generate_id(audits)
        rec = {
            "audit_id": aid,
            "actor_user_id": str(actor_user_id),
            "reference_type": reference_type,
            "reference_id": str(reference_id),
            "action": action,
            "summary": summary,
            "created_at": TS
        }
        audits[aid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        ref_allowed = "user|client|component|incident|problem|change_request|work_order|escalation|workaround|rca|communication|status_history|report|metric|knowledge|pir|approval"
        act_allowed = "create|read|update|delete|approve|reject|status_change|link|generate"
        return {
            "type":"function",
            "function":{
                "name":"create_audit_entry",
                "description":"Write an audit entry capturing actor, reference, action, and summary.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "actor_user_id":{"type":"string","description":"User ID of the actor (required)"},
                        "reference_type":{"type":"string","description":f"Enum: {ref_allowed} (required)"},
                        "reference_id":{"type":"string","description":"ID of the referenced record (required)"},
                        "action":{"type":"string","description":f"Enum: {act_allowed} (required)"},
                        "summary":{"type":"string","description":"Bounded summary of inputs/intent (required)"}
                    },
                    "required":["actor_user_id","reference_type","reference_id","action","summary"]
                }
            }
        }
