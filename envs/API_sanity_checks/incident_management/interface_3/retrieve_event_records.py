
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


class RetrieveEventRecords(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               event_id: Optional[str] = None,
               source: Optional[str] = None,
               severity_hint: Optional[str] = None,
               detected_from: Optional[str] = None,
               detected_to: Optional[str] = None) -> str:
        evs = data.get("event_records", {})
        out = []

        if event_id:
            rec = evs.get(str(event_id))
            return json.dumps([rec] if rec else [])

        for r in evs.values():
            if source and r.get("source") != source:
                continue
            if severity_hint and r.get("severity_hint") != severity_hint:
                continue
            # detected_from/to are strings; simple lexical filter is fine for the fixed TS
            if detected_from and str(r.get("detected_at")) < detected_from:
                continue
            if detected_to and str(r.get("detected_at")) > detected_to:
                continue
            out.append(r)
        return json.dumps(out)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"retrieve_event_records",
                "description":"List event records with filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "event_id":{"type":"string","description":"Optional event id"},
                        "source":{"type":"string","description":"Optional source filter"},
                        "severity_hint":{"type":"string","description":"Optional severity: P1|P2|P3|P4"},
                        "detected_from":{"type":"string","description":"Optional ISO from"},
                        "detected_to":{"type":"string","description":"Optional ISO to"}
                    },
                    "required":[]
                }
            }
        }
