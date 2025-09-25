############################################################
# 12) Add_knowledge_article.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddKnowledgeArticle(Tool):
    """
    Creates a Draft knowledge article, optionally linked to an incident.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        creating_user_id: str,
        title: str,
        content_type: str,
        category: str,
        incident_id: Optional[str] = None,
        reviewer_id: Optional[str] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        kbs = data.get("knowledge_articles", {})

        if str(creating_user_id) not in users:
            return json.dumps({"error": f"User {creating_user_id} not found", "halt": True})
        if incident_id is not None and str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})
        if reviewer_id is not None and str(reviewer_id) not in users:
            return json.dumps({"error": f"Reviewer {reviewer_id} not found", "halt": True})

        ct_allowed = ['how_to','troubleshooting','postmortem','reference']
        cat_allowed = ['infrastructure','application','network','security','general']
        if content_type not in ct_allowed:
            return json.dumps({"error": f"Invalid content_type. Allowed: {ct_allowed}", "halt": True})
        if category not in cat_allowed:
            return json.dumps({"error": f"Invalid category. Allowed: {cat_allowed}", "halt": True})

        kid = AddKnowledgeArticle._generate_id(kbs)
        rec = {
            "kb_id": kid,
            "creating_user_id": str(creating_user_id),
            "incident_id": str(incident_id) if incident_id is not None else None,
            "title": title,
            "content_type": content_type,
            "category": category,
            "status": "draft",
            "reviewer_user_id": str(reviewer_id) if reviewer_id is not None else None,
            "created_at": TS,
            "updated_at": TS
        }
        kbs[kid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        ct_allowed = "how_to|troubleshooting|postmortem|reference"
        cat_allowed = "infrastructure|application|network|security|general"
        return {
            "type":"function",
            "function":{
                "name":"create_knowledge_article",
                "description":"Create a Draft knowledge article, optionally linking it to an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "creating_user_id":{"type":"string","description":"User ID creating the article (required)"},
                        "title":{"type":"string","description":"Article title (required)"},
                        "content_type":{"type":"string","description":f"Enum: {ct_allowed} (required)"},
                        "category":{"type":"string","description":f"Enum: {cat_allowed} (required)"},
                        "incident_id":{"type":"string","description":"Incident ID to link (optional)"},
                        "reviewer_id":{"type":"string","description":"Reviewer user ID (optional)"}
                    },
                    "required":["creating_user_id","title","content_type","category"]
                }
            }
        }
