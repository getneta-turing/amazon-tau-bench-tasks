
############################################################
# 10) add_metric.py
############################################################
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddMetric(Tool):
    """
    Stores performance metrics (e.g., MTTA/MTTR) for a Closed incident.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        metric_type: str,
        value_minutes: int,
        target_minutes: Optional[int] = None
    ) -> str:
        TS = "2025-10-01T00:00:00"
        incidents = data.get("incidents", {})
        metrics = data.get("metrics", {})

        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found", "halt": True})

        inc = incidents[str(incident_id)]
        if inc.get("status") != "closed":
            return json.dumps({"error": "Incident must be in 'closed' status to record performance metrics", "halt": True})

        allowed = ['MTTA','MTTR','MTTD','time_to_comm']
        if metric_type not in allowed:
            return json.dumps({"error": f"Invalid metric_type. Allowed: {allowed}", "halt": True})

        mid = AddMetric._generate_id(metrics)
        rec = {
            "metric_id": mid,
            "incident_id": str(incident_id),
            "metric_type": metric_type,
            "value_minutes": int(value_minutes),
            "target_minutes": int(target_minutes) if target_minutes is not None else None,
            "computed_at": TS
        }
        metrics[mid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_metric_record",
                "description":"Create a performance metric record for a CLOSED incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Closed incident ID (required)"},
                        "metric_type":{"type":"string","description":"Enum: MTTA|MTTR|MTTD|time_to_comm (required)"},
                        "value_minutes":{"type":"integer","description":"Metric value in minutes (required)"},
                        "target_minutes":{"type":"integer","description":"Target value in minutes (optional)"}
                    },
                    "required":["incident_id","metric_type","value_minutes"]
                }
            }
        }
