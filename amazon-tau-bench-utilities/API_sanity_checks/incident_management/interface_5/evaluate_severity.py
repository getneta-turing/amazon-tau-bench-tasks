
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


class EvaluateSeverity(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               complete_outage: Optional[bool] = None,
               client_count_impacted: Optional[int] = None,
               has_workaround: Optional[bool] = None,
               regulatory_or_financial_impact: Optional[bool] = None,
               is_priority_client: Optional[bool] = None) -> str:
        # Simple heuristic
        if complete_outage is True or (client_count_impacted or 0) > 50:
            suggested = "P1"
        elif (client_count_impacted or 0) > 10 or regulatory_or_financial_impact is True:
            suggested = "P2"
        elif has_workaround is True:
            suggested = "P3"
        else:
            suggested = "P4"
        return json.dumps({"suggested_severity": suggested})

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"evaluate_severity",
                "description":"Classify severity P1–P4 from provided criteria snapshot.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "complete_outage":{"type":"boolean","description":"(True/False) Service is fully down"},
                        "client_count_impacted":{"type":"integer","description":"Number of clients affected"},
                        "has_workaround":{"type":"boolean","description":"(True/False) Temporary mitigation exists"},
                        "regulatory_or_financial_impact":{"type":"boolean","description":"(True/False) Regulatory/financial impact"},
                        "is_priority_client":{"type":"boolean","description":"(True/False) Priority client involved"}
                    },
                    "required":[]
                }
            }
        }
