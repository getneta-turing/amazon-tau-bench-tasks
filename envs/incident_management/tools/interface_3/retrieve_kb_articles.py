
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"
class RetrieveKbArticles(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               article_id: Optional[str] = None,
               category: Optional[str] = None,
               status: Optional[str] = None) -> str:
        kbs = data.get("knowledge_base_articles", {})
        out = []
        if article_id:
            rec = kbs.get(str(article_id))
            return json.dumps([rec] if rec else [])
        for r in kbs.values():
            if category and r.get("category") != category:
                continue
            if status and r.get("status") != status:
                continue
            out.append(r)
        return json.dumps(out)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"retrieve_kb_articles",
                "description":"Retrieve knowledge articles by filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "article_id":{"type":"string","description":"Optional article id"},
                        "category":{"type":"string","description":"Optional category"},
                        "status":{"type":"string","description":"Optional: draft|published|archived"}
                    },
                    "required":[]
                }
            }
        }
