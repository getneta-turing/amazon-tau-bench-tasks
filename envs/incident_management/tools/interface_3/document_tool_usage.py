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
class DocumentToolUsage(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        tool_used: str,
        action_summary: str,
        executed_by: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(executed_by) not in users:
            return json.dumps({"error": f"User {executed_by} not found"})
        allowed = ["monitoring","root_cause_analysis","ITSM_service_desk","incident_response","AI_virtual_agent","AIOps","automation_script"]
        if tool_used not in allowed:
            return json.dumps({"error": f"Invalid tool_used. Allowed: {allowed}"})
        tus = data.setdefault("tool_usages", {})
        tid = _generate_id(tus)
        rec = {
            "tool_usage_id": str(tid),
            "incident_id": str(incident_id),
            "tool_used": tool_used,
            "action_summary": action_summary,
            "executed_by_user_id": str(executed_by),
            "executed_at": TIMESTAMP,
            "outcome": "noted"
        }
        tus[str(tid)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"document_tool_usage",
                "description":"Record the use of a tool/automation outcome (no external execution).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "tool_used":{"type":"string","description":"Allowed: monitoring, root_cause_analysis, ITSM_service_desk, incident_response, AI_virtual_agent, AIOps, automation_script"},
                        "action_summary":{"type":"string","description":"Summary of the action"},
                        "executed_by":{"type":"string","description":"User ID who executed the tool/action"}
                    },
                    "required":["incident_id","tool_used","action_summary","executed_by"]
                }
            }
        }
