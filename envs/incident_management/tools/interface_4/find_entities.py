
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"
class FindEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, requester_id: str, filters: Optional[Dict[str, Any]] = None) -> str:
        users = data.get("users", {})
        if str(requester_id) not in users:
            return json.dumps({"error": f"Requester {requester_id} not found"})

        mapping = {
            "incident": "incidents",
            "user": "users",
            "service": "services",
            "problem": "problems",
            "vendor_engagement": "vendor_engagements",
            "change": "change_requests",
            "kb_entry": "knowledge_base_articles",
            "monitoring_event": "monitoring_events",
        }
        if entity_type not in mapping:
            return json.dumps({"error": "Invalid entity_type. Must be one of: incident,user,service,problem,vendor_engagement,change,kb_entry,monitoring_event"})

        table = data.get(mapping[entity_type], {})
        if not isinstance(table, dict):
            return json.dumps([])

        filters = filters or {}
        results = []
        for rec in table.values():
            ok = True
            for k, v in filters.items():
                if rec.get(k) != v:
                    ok = False
                    break
            if ok:
                results.append(rec)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_entities",
                "description": "Find/verify incidents, users, services/systems, problems, vendor engagements, changes, KB entries, or monitoring events before taking another action.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Entity type to search. Allowed: incident, user, service, problem, vendor_engagement, change, kb_entry, monitoring_event"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional exact-match filters to apply (only keys you actually have)."
                        },
                        "requester_id": {
                            "type": "string",
                            "description": "ID of the user requesting the lookup"
                        }
                    },
                    "required": ["entity_type", "requester_id"]
                }
            }
        }

