
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


class RecordMetricEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               incident_id: str,
               metric_type: str,
               calculated_value_minutes: int,
               target_minutes: Optional[int] = None) -> str:
        incidents = data.get("incidents", {})
        metrics = data.get("metrics", {})
        allowed = ["mean_time_to_detect","mean_time_to_acknowledge","mean_time_to_resolve","mean_time_between_failures","sla_breach_rate"]

        if not _ensure_exists(incidents, incident_id):
            return json.dumps({"error":"incident_id not found"})
        if metric_type not in allowed:
            return json.dumps({"error":"Invalid metric_type. Allowed: " + "|".join(allowed)})
        if calculated_value_minutes is None:
            return json.dumps({"error":"calculated_value_minutes is required"})

        mid = _generate_id(metrics)
        row = {
            "metric_id": mid,
            "incident_id": incident_id,
            "metric_type": metric_type,
            "value_minutes": int(calculated_value_minutes),
            "target_minutes": None if target_minutes is None else int(target_minutes),
            "recorded_by_id": None,
            "recorded_at": TS
        }
        metrics[mid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"record_metric",
                "description":"Store performance metrics for a closed incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID (required)"},
                        "metric_type":{"type":"string","description":"Required: mean_time_to_detect|mean_time_to_acknowledge|mean_time_to_resolve|mean_time_between_failures|sla_breach_rate"},
                        "calculated_value_minutes":{"type":"integer","description":"Value in minutes (required)"},
                        "target_minutes":{"type":"integer","description":"Optional target in minutes"}
                    },
                    "required":["incident_id","metric_type","calculated_value_minutes"]
                }
            }
        }
