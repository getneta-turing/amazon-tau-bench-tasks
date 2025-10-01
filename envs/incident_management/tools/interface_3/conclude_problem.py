#!/usr/bin/env bash

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"
class ConcludeProblem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        problem_id: str,
        closed_by_user_id: str,
        closure_notes: str
    ) -> str:
        probs = data.get("problems", {})
        users = data.get("users", {})
        if str(problem_id) not in probs:
            return json.dumps({"error": f"Problem {problem_id} not found"})
        if str(closed_by_user_id) not in users:
            return json.dumps({"error": f"User {closed_by_user_id} not found"})
        prob = probs[str(problem_id)]
        if prob.get("status") != "resolved":
            return json.dumps({"error": "Problem must be in resolved status before closing"})

        prob["status"] = "closed"
        prob["closed_by_user_id"] = str(closed_by_user_id)
        prob["closed_at"] = TIMESTAMP
        prob["closure_notes"] = closure_notes
        probs[str(problem_id)] = prob
        return json.dumps(prob)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"conculde_problem",
                "description":"Close a resolved problem.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "problem_id":{"type":"string","description":"Problem ID"},
                        "closed_by_user_id":{"type":"string","description":"User ID who closes the problem"},
                        "closure_notes":{"type":"string","description":"Closure notes"}
                    },
                    "required":["problem_id","closed_by_user_id","closure_notes"]
                }
            }
        }
