############################################################
# 1) search_entities.py
############################################################

import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool


class DiscoverRecords(Tool):
    """
    Policy-compliant lookup for any IMS entity type with optional filters and requester authorization presence check.
    """

    @staticmethod
    def _generate_summary(item: Dict[str, Any], key_fields: List[str]) -> Dict[str, Any]:
        out = {}
        for k in key_fields:
            if k in item:
                out[k] = item[k]
        return out

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        requester_id: str,
        filters: Optional[Dict[str, Any]] = None,
        approval_reference: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"

        allowed_entities = {
            "user": ("users", ["user_id", "full_name", "email", "role", "status"]),
            "client": ("clients", ["client_id", "legal_name", "status"]),
            "component": ("components", ["component_id", "name", "client_id", "status"]),
            "incident": ("incidents", ["incident_id", "title", "severity", "status", "client_id"]),
            "problem": ("problem_tickets", ["problem_id", "incident_id", "title", "status"]),
            "change_request": ("change_requests", ["change_id", "incident_id", "title", "status", "risk"]),
            "work_order": ("work_orders", ["work_order_id", "change_id", "title", "status"]),
            "workaround": ("workarounds", ["workaround_id", "incident_id", "status", "effectiveness"]),
            "rca": ("root_cause_analyses", ["rca_id", "incident_id", "analysis_method", "status"]),
            "communication": ("communications", ["communication_id", "incident_id", "communication_type", "delivery_status"]),
            "report": ("reports", ["report_id", "incident_id", "report_type", "status"]),
            "metric": ("metrics", ["metric_id", "incident_id", "metric_type", "value_minutes"]),
            "knowledge": ("knowledge_articles", ["kb_id", "title", "status", "category"]),
            "pir": ("post_incident_reviews", ["pir_id", "incident_id", "scheduled_date", "status"]),
        }

        # Basic authorization presence check
        users = data.get("users", {})
        if str(requester_id) not in users:
            return json.dumps({"error": f"Requester {requester_id} not found", "halt": True})

        if entity_type not in allowed_entities:
            return json.dumps({"error": f"Invalid entity_type. Allowed: {list(allowed_entities.keys())}", "halt": True})

        table_name, key_fields = allowed_entities[entity_type]
        table = data.get(table_name, {})
        filters = filters or {}

        # Apply filters (exact match on provided keys)
        results: List[Dict[str, Any]] = []
        for rec in table.values():
            ok = True
            for fk, fv in filters.items():
                if rec.get(fk) != fv:
                    ok = False
                    break
            if ok:
                results.append(rec)

        if len(results) == 0:
            return json.dumps([])

        if len(results) == 1:
            return json.dumps(results)

        # Multiple results → summaries for disambiguation
        summaries = [DiscoverRecords._generate_summary(
            r, key_fields) for r in results]
        return json.dumps(summaries)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_entities",
                "description": "Policy-compliant lookup for an IMS entity. Returns full records on single match; returns brief summaries on multiple matches; empty array if none.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "One of: user|client|component|incident|problem|change_request|work_order|workaround|rca|communication|report|metric|knowledge|pir"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional key/value exact-match filters; only provided keys are applied"
                        },
                        "requester_id": {
                            "type": "string",
                            "description": "ID of the requester performing the lookup"
                        },
                        "approval_reference": {
                            "type": "string",
                            "description": "Approval reference if protected data requires it (optional)"
                        }
                    },
                    "required": ["entity_type", "requester_id"]
                }
            }
        }
