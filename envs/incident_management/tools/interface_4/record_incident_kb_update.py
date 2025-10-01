
import json
from typing import Any, Dict
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
class RecordIncidentKbUpdate(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        kb_update_notes: str,
        submitted_by_user_id: str
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(submitted_by_user_id) not in users:
            return json.dumps({"error": f"User {submitted_by_user_id} not found"})

        kbs = data.setdefault("knowledge_base_articles", {})
        kb_id = _generate_id(kbs)
        kbs[str(kb_id)] = {
            "kb_id": str(kb_id),
            "title": f"KB from Incident {incident_id}",
            "content_summary": kb_update_notes,
            "status": "published",
            "created_by_user_id": str(submitted_by_user_id),
            "created_at": TIMESTAMP,
            "updated_at": TIMESTAMP
        }

        links = data.setdefault("kb_links", {})
        l_id = _generate_id(links)
        links[str(l_id)] = {
            "kb_link_id": str(l_id),
            "kb_id": str(kb_id),
            "reference_type": "incident",
            "reference_id": str(incident_id),
            "linked_by_user_id": str(submitted_by_user_id),
            "linked_at": TIMESTAMP
        }

        return json.dumps(kbs[str(kb_id)])

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"record_incident_kb_update",
                "description":"Add or update KB entries with resolutions/workarounds/preventive measures linked to an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "kb_update_notes":{"type":"string","description":"Notes to publish to KB"},
                        "submitted_by_user_id":{"type":"string","description":"User ID submitting the KB update"}
                    },
                    "required":["incident_id","kb_update_notes","submitted_by_user_id"]
                }
            }
        }
