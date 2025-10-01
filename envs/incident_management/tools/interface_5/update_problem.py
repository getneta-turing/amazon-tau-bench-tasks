#!/usr/bin/env bash

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"

class UpdateProblem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        problem_id: str,
        change_set: Dict[str, Any],
        updated_by_user_id: str
    ) -> str:
        probs = data.get("problems", {})
        users = data.get("users", {})
        if str(problem_id) not in probs:
            return json.dumps({"error": f"Problem {problem_id} not found"})
        if str(updated_by_user_id) not in users:
            return json.dumps({"error": f"User {updated_by_user_id} not found"})

        allowed_fields = {"title", "description"}
        rec = probs[str(problem_id)]
        for k, v in change_set.items():
            if k in allowed_fields:
                rec[k] = v
        probs[str(problem_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"Update_problem",
                "description":"Update mutable fields on a problem (title, description).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "problem_id":{"type":"string","description":"Problem ID"},
                        "change_set":{"type":"object","description":"Allowed keys: title, description"},
                        "updated_by_user_id":{"type":"string","description":"User ID performing the update"}
                    },
                    "required":["problem_id","change_set","updated_by_user_id"]
                }
            }
        }
