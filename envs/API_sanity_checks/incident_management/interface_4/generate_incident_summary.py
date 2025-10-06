
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


class GenerateIncidentSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               report_type: str,
               generated_by: str) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        reports = data.get("incident_reports", {})
        allowed = ["executive_summary","postmortem_report","compliance_report","performance_dashboard","trend_analysis"]

        if not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if report_type not in allowed:
            return json.dumps({"error":"Invalid report_type. Allowed: " + "|".join(allowed)})
        if not _ensure_exists(users, generated_by):
            return json.dumps({"error":"generated_by not found"})

        rid = _generate_id(reports)
        row = {
            "report_id": rid,
            "incident_id": incident_id,
            "report_type": report_type,
            "generated_by_id": generated_by,
            "status": "completed",
            "generated_at": TS
        }
        reports[rid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"generate_incident_report",
                "description":"Produce formal incident documentation.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "report_type":{"type":"string","description":"Required: executive_summary|postmortem_report|compliance_report|performance_dashboard|trend_analysis"},
                        "generated_by":{"type":"string","description":"User ID (required)"}
                    },
                    "required":["incident_id","report_type","generated_by"]
                }
            }
        }
