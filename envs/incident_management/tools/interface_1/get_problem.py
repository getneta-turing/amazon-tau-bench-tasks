#!/usr/bin/env bash

import json
from typing import Any, Dict, Optional, List
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







class GetProblem(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], problem_id: str) -> str:
        probs = data.get("problems", {})
        rec = probs.get(str(problem_id))
        if not rec:
            return json.dumps({"error": f"Problem {problem_id} not found"})
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"get_problem",
                "description":"Fetch a single problem by ID, including linked incidents/KB (links not expanded here).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "problem_id":{"type":"string","description":"Problem ID"}
                    },
                    "required":["problem_id"]
                }
            }
        }
