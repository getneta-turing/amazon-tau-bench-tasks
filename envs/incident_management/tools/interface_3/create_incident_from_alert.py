
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
class CreateIncidentFromAlert(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        monitoring_event_id: str,
        detected_service: str,
        alert_details: str
    ) -> str:
        events = data.get("monitoring_events", {})
        services = data.get("services", {})
        if str(monitoring_event_id) not in events:
            return json.dumps({"error": f"Monitoring event {monitoring_event_id} not found"})
        if str(detected_service) not in services:
            return json.dumps({"error": f"Service {detected_service} not found"})
        ev = events[str(monitoring_event_id)]

        incidents = data.setdefault("incidents", {})
        new_id = _generate_id(incidents)
        rec = {
            "incident_id": str(new_id),
            "reporter_id": ev.get("created_by_user_id"),
            "detection_source": ev.get("source", "monitoring_tool"),
            "category": "other",
            "priority": "medium",
            "severity": ev.get("severity", "medium"),
            "status": "open",
            "affected_service_id": str(detected_service),
            "initial_description": f"{ev.get('alert_type')}: {alert_details}",
            "source_event_id": str(monitoring_event_id),
            "created_at": TIMESTAMP,
            "resolved_at": None,
            "closed_at": None,
            "resolved_by_user_id": None,
            "closed_by_user_id": None
        }
        incidents[str(new_id)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"create_incident_from_alert",
                "description":"Convert an existing IMS monitoring/alert record into a new incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "monitoring_event_id":{"type":"string","description":"Existing monitoring_events.event_id"},
                        "detected_service":{"type":"string","description":"services.service_id that was detected"},
                        "alert_details":{"type":"string","description":"Details from alert"}
                    },
                    "required":["monitoring_event_id","detected_service","alert_details"]
                }
            }
        }
