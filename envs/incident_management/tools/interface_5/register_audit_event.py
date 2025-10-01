#!/usr/bin/env bash

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


class RegisterAuditEvent(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        action: str,
        reference_type: str,
        reference_id: str,
        meta: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})

        allowed_actions = ["identify","create","read","update","escalate","notify","resolve","close","review","kb_update","vendor_engagement","simulation","tool_use"]
        if action not in allowed_actions:
            return json.dumps({"error": f"Invalid action. Allowed: {allowed_actions}"})
        allowed_refs = ["incident","communication","review","kb","tool_use","vendor","problem"]
        if reference_type not in allowed_refs:
            return json.dumps({"error": f"Invalid reference_type. Allowed: {allowed_refs}"})

        aud = data.setdefault("audit_trails", {})
        aid = _generate_id(aud)
        rec = {
            "audit_trail_id": str(aid),
            "reference_type": reference_type,
            "reference_id": str(reference_id),
            "action": action,
            "user_id": str(user_id),
            "field_name": None,
            "old_value": None,
            "new_value": meta,
            "created_at": TIMESTAMP
        }
        aud[str(aid)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"register_audit_event",
                "description":"Write an audit entry for any access-controlled read or state change.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "user_id":{"type":"string","description":"User performing action"},
                        "action":{"type":"string","description":"Allowed: identify, create, read, update, escalate, notify, resolve, close, review, kb_update, vendor_engagement, simulation, tool_use"},
                        "reference_type":{"type":"string","description":"Allowed: incident, communication, review, kb, tool_use, vendor, problem"},
                        "reference_id":{"type":"string","description":"ID of referenced record"},
                        "meta":{"type":"string","description":"Optional terse context"}
                    },
                    "required":["user_id","action","reference_type","reference_id"]
                }
            }
        }
