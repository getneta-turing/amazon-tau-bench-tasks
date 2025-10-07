
import json
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool

TS = "2025-10-01T00:00:00"


class HandoffToHuman(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               reason_code: str,
               details: Optional[str] = None) -> str:
        if not reason_code:
            return json.dumps({"error":"reason_code is required"})
        return json.dumps({"success": True, "message": "Transferred to human", "reason_code": reason_code, "details": details})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"handoff_to_human",
                "description":"Escalate the current request to a human operator when a halt condition is met.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "reason_code":{"type":"string","description":"Brief code (required)"},
                        "details":{"type":"string","description":"Short explanation (optional)"}
                    },
                    "required":["reason_code"]
                }
            }
        }
