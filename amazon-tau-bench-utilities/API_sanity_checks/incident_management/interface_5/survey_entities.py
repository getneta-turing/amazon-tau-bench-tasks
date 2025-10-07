import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class SurveyEntities(Tool):
    @staticmethod
    def _as_str(x):
        return None if x is None else str(x)

    @staticmethod
    def _filter_rows(rows: Dict[str, Any], filters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not filters:
            return list(rows.values())
        out = []
        for rec in rows.values():
            ok = True
            for k, v in filters.items():
                rv = rec.get(k)
                if isinstance(v, str):
                    # case-insensitive match if string
                    if rv is None or str(rv).lower() != v.lower():
                        ok = False
                        break
                else:
                    if rv != v:
                        ok = False
                        break
            if ok:
                out.append(rec)
        return out

    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None,
               requester_id: str = "") -> str:
        # Validate allowed entity types
        allowed = {
            "client":"clients","user":"users","vendor":"vendors","product":"products","component":"components",
            "subscription":"subscriptions","sla":"sla_agreements","incident":"incidents","workaround":"workarounds",
            "rca":"root_cause_analyses","escalation":"escalations","change_request":"change_requests",
            "rollback_request":"rollback_requests","metric":"metrics","incident_report":"incident_reports",
            "kb_article":"knowledge_base_articles","post_incident_review":"post_incident_reviews",
            "event_record":"event_records"
        }
        key = allowed.get(entity_type)
        if not key:
            return json.dumps({"error": "Invalid entity_type. Must be one of client|user|vendor|product|component|subscription|sla|incident|workaround|rca|escalation|change_request|rollback_request|metric|incident_report|kb_article|post_incident_review|event_record"})

        table = data.get(key, {})
        # requester_id existence is not enforced here (discovery can be anonymous), per "search/get" nature
        results = DiscoverEntities._filter_rows(table, filters)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "survey_entities",
                "description": "Search for and verify entities (client|user|vendor|product|component|subscription|sla|incident|workaround|rca|escalation|change_request|rollback_request|metric|incident_report|kb_article|post_incident_review|event_record). Returns an array of matches.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "One of: client|user|vendor|product|component|subscription|sla|incident|workaround|rca|escalation|change_request|rollback_request|metric|incident_report|kb_article|post_incident_review|event_record"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filter dict with fields known to the chosen entity"
                        },
                        "requester_id": {
                            "type": "string",
                            "description": "User performing discovery (optional)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
