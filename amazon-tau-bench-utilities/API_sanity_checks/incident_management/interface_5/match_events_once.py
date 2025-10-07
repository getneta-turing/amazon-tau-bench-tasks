
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


class MatchEventsOnce(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               event_ids: List[str],
               correlation_key: str,
               link_incident_id: Optional[str] = None) -> str:
        event_records = data.get("event_records", {})
        event_correlations = data.get("event_correlations", {})
        incidents = data.get("incidents", {})

        if not event_ids:
            return json.dumps({"error": "event_ids is required and must be non-empty"})

        for eid in event_ids:
            if not _ensure_exists(event_records, eid):
                return json.dumps({"error": f"event_id {eid} not found"})

        if link_incident_id is not None and not _ensure_exists(incidents, link_incident_id):
            return json.dumps({"error": "link_incident_id not found"})

        out = []
        for eid in event_ids:
            cid = _generate_id(event_correlations)
            row = {
                "correlation_id": cid,
                "event_id": eid,
                "correlation_key": correlation_key,
                "incident_id": str(link_incident_id) if link_incident_id else None,
                "created_at": TS
            }
            event_correlations[cid] = row
            out.append(row)
        return json.dumps(out)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"correlate_events_once",
                "description":"One-time correlation of provided events in the current interaction.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "event_ids":{"type":"array","description":"List of event IDs to correlate (required)","items":{"type":"string"}},
                        "correlation_key":{"type":"string","description":"Rule/key used (required)"},
                        "link_incident_id":{"type":"string","description":"Optional existing incident to link"}
                    },
                    "required":["event_ids","correlation_key"]
                }
            }
        }
