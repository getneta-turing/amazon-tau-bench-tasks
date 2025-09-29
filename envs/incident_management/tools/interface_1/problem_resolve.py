import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"




class ProblemResolve(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        problem_id: str,
        permanent_fix_summary: str,
        validation_evidence: str,
        resolved_by_user_id: str
    ) -> str:
        probs = data.get("problems", {})
        users = data.get("users", {})
        if str(problem_id) not in probs:
            return json.dumps({"error": f"Problem {problem_id} not found"})
        if str(resolved_by_user_id) not in users:
            return json.dumps({"error": f"User {resolved_by_user_id} not found"})

        prob = probs[str(problem_id)]
        prob["status"] = "resolved"
        prob["resolved_by_user_id"] = str(resolved_by_user_id)
        prob["resolved_at"] = TIMESTAMP
        prob["permanent_fix_summary"] = permanent_fix_summary
        prob["validation_evidence"] = validation_evidence
        probs[str(problem_id)] = prob
        return json.dumps(prob)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"problem_resolve",
                "description":"Record a permanent fix with validation evidence; set status resolved.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "problem_id":{"type":"string","description":"Problem ID"},
                        "permanent_fix_summary":{"type":"string","description":"Summary of the permanent fix"},
                        "validation_evidence":{"type":"string","description":"Validation evidence details"},
                        "resolved_by_user_id":{"type":"string","description":"User ID who resolved the problem"}
                    },
                    "required":["problem_id","permanent_fix_summary","validation_evidence","resolved_by_user_id"]
                }
            }
        }
