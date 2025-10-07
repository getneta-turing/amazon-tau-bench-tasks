
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


class CommenceRca(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               analysis_method: str,
               assigned_to: str) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        rcas = data.get("root_cause_analyses", {})

        allowed = ["five_whys","fishbone_diagram","fault_tree_analysis","cause_effect_matrix","pareto_analysis"]

        if not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if analysis_method not in allowed:
            return json.dumps({"error":"Invalid analysis_method. Allowed: five_whys|fishbone_diagram|fault_tree_analysis|cause_effect_matrix|pareto_analysis"})
        if not _ensure_exists(users, assigned_to):
            return json.dumps({"error":"assigned_to not found"})

        rid = _generate_id(rcas)
        row = {
            "rca_id": rid,
            "incident_id": incident_id,
            "conducted_by_id": assigned_to,
            "analysis_method": analysis_method,
            "status": "in_progress",
            "summary": None,
            "completed_at": None,
            "created_at": TS
        }
        rcas[rid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"commence_rca",
                "description":"Initiate root-cause analysis.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "analysis_method":{"type":"string","description":"Required: five_whys|fishbone_diagram|fault_tree_analysis|cause_effect_matrix|pareto_analysis"},
                        "assigned_to":{"type":"string","description":"User ID (required)"}
                    },
                    "required":["incident_id","analysis_method","assigned_to"]
                }
            }
        }
