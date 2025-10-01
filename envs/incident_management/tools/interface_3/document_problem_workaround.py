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




class DocumentProblemWorkaround(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        problem_id: str,
        workaround_summary: str,
        added_by_user_id: str
    ) -> str:
        probs = data.get("problems", {})
        users = data.get("users", {})
        if str(problem_id) not in probs:
            return json.dumps({"error": f"Problem {problem_id} not found"})
        if str(added_by_user_id) not in users:
            return json.dumps({"error": f"User {added_by_user_id} not found"})

        pwa = data.setdefault("problem_workarounds", {})
        wid = _generate_id(pwa)
        pwa[str(wid)] = {
            "workaround_id": str(wid),
            "problem_id": str(problem_id),
            "summary": workaround_summary,
            "added_by_user_id": str(added_by_user_id),
            "added_at": TIMESTAMP,
            "active": True
        }

        # Update problem status and known_error
        prob = probs[str(problem_id)]
        prob["status"] = "workaround_available"
        prob["known_error"] = True
        probs[str(problem_id)] = prob

        # Publish to KB
        kbs = data.setdefault("knowledge_base_articles", {})
        kb_id = _generate_id(kbs)
        kbs[str(kb_id)] = {
            "kb_id": str(kb_id),
            "title": f"Workaround for Problem {problem_id}",
            "content_summary": workaround_summary,
            "status": "published",
            "created_by_user_id": str(added_by_user_id),
            "created_at": TIMESTAMP,
            "updated_at": TIMESTAMP
        }
        links = data.setdefault("kb_links", {})
        l_id = _generate_id(links)
        links[str(l_id)] = {
            "kb_link_id": str(l_id),
            "kb_id": str(kb_id),
            "reference_type": "problem",
            "reference_id": str(problem_id),
            "linked_by_user_id": str(added_by_user_id),
            "linked_at": TIMESTAMP
        }

        return json.dumps(probs[str(problem_id)])

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"document_problem_workaround",
                "description":"Record a workaround; set status to workaround_available and publish to KB.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "problem_id":{"type":"string","description":"Problem ID"},
                        "workaround_summary":{"type":"string","description":"Workaround summary"},
                        "added_by_user_id":{"type":"string","description":"User ID who adds the workaround"}
                    },
                    "required":["problem_id","workaround_summary","added_by_user_id"]
                }
            }
        }
