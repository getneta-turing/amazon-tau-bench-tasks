
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


class IngestEventRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               source: str,
               payload_summary: str,
               severity_hint: Optional[str] = None,
               recorded_by_id: Optional[str] = None) -> str:
        events = data.get("event_records", {})
        users  = data.get("users", {})

        allowed_sources = ["alert_log","incident_portal_submission","internal_tool"]
        allowed_sev = ["P1","P2","P3","P4"]

        if source not in allowed_sources:
            return json.dumps({"error": "Invalid source. Allowed: alert_log|incident_portal_submission|internal_tool"})
        if not payload_summary:
            return json.dumps({"error": "payload_summary is required"})

        if severity_hint is not None and severity_hint not in allowed_sev:
            return json.dumps({"error": "Invalid severity_hint. Allowed: P1|P2|P3|P4"})

        if recorded_by_id is not None and not _ensure_exists(users, recorded_by_id):
            return json.dumps({"error": "recorded_by_id not found"})

        event_id = _generate_id(events)
        new_row = {
            "event_id": event_id,
            "source": source,
            "payload_summary": payload_summary,
            "severity_hint": severity_hint,
            "detected_at": TS,
            "recorded_by_id": recorded_by_id,
            "created_at": TS
        }
        events[event_id] = new_row
        return json.dumps(new_row)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"ingest_event_record",
                "description":"Store a user-provided alert/event into the internal DB.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "source":{"type":"string","description":"One of: alert_log|incident_portal_submission|internal_tool (required)"},
                        "payload_summary":{"type":"string","description":"Concise summary (required)"},
                        "severity_hint":{"type":"string","description":"Optional severity hint: P1|P2|P3|P4"},
                        "recorded_by_id":{"type":"string","description":"Optional user ID who provided/loaded the event"}
                    },
                    "required":["source","payload_summary"]
                }
            }
        }
