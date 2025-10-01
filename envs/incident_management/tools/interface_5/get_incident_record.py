#!/usr/bin/env bash

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"

class GetIncidentRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str) -> str:
        incidents = data.get("incidents", {})
        rec = incidents.get(str(incident_id))
        if not rec:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"get_incident_record",
                "description":"Fetch a single incident by ID (access-controlled read).",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"}
                    },
                    "required":["incident_id"]
                }
            }
        }
