#!/usr/bin/env bash

import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"




class GetIncidentCommunications(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str) -> str:
        communications = data.get("communications", {})
        results = [c for c in communications.values() if c.get("incident_id") == str(incident_id)]
        return json.dumps(results)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"get_incident_communications",
                "description":"Retrieve communications for an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"}
                    },
                    "required":["incident_id"]
                }
            }
        }
