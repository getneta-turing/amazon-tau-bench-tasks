
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"

def _generate_id(table: Dict[str, Any]) -> str:
    if not table:
        return "1"
    try:
        mx = max(int(k) for k in table.keys())
    except Exception:
        # fallback in case keys are not purely numeric strings
        nums = []
        for k in table.keys():
            try:
                nums.append(int(k))
            except:
                pass
        mx = max(nums) if nums else 0
    return str(mx + 1)

def _enum_ok(value: Optional[str], allowed: List[str]) -> bool:
    if value is None:
        return False
    return value in allowed

def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class PublishKbArticle(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               title: str,
               content_type: str,
               category: str,
               author_id: str,
               incident_id: Optional[str] = None,
               reviewer_user_id: Optional[str] = None) -> str:
        users = data.get("users", {})
        incidents = data.get("incidents", {})
        kbs = data.get("knowledge_base_articles", {})
        ctypes = ["troubleshooting","resolution_steps","prevention_guide","faq"]
        cats = ["incident_resolution","problem_management","change_management","troubleshooting","best_practice"]

        if not title or not content_type or not category or not author_id:
            return json.dumps({"error":"title, content_type, category, author_id are required"})
        if content_type not in ctypes:
            return json.dumps({"error":"Invalid content_type"})
        if category not in cats:
            return json.dumps({"error":"Invalid category"})
        if not _ensure_exists(users, author_id):
            return json.dumps({"error":"author_id not found"})
        if reviewer_user_id is not None and not _ensure_exists(users, reviewer_user_id):
            return json.dumps({"error":"reviewer_user_id not found"})
        if incident_id is not None and not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})

        aid = _generate_id(kbs)
        row = {
            "article_id": aid,
            "title": title,
            "content_type": content_type,
            "category": category,
            "author_id": author_id,
            "reviewer_user_id": reviewer_user_id,
            "incident_id": incident_id,
            "status": "draft",
            "view_count": 0,
            "created_at": TS,
            "updated_at": TS
        }
        kbs[aid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"publish_kb_article",
                "description":"Document a resolution/best practice.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "title":{"type":"string","description":"Title (required)"},
                        "content_type":{"type":"string","description":"Required: troubleshooting|resolution_steps|prevention_guide|faq"},
                        "category":{"type":"string","description":"Required: incident_resolution|problem_management|change_management|troubleshooting|best_practice"},
                        "author_id":{"type":"string","description":"Author user id (required)"},
                        "incident_id":{"type":"string","description":"Optional incident id"},
                        "reviewer_user_id":{"type":"string","description":"Optional reviewer user id"}
                    },
                    "required":["title","content_type","category","author_id"]
                }
            }
        }
