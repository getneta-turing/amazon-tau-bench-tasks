
#!/usr/bin/env bash

import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

TIMESTAMP = "2025-10-01T00:00:00"
class BrowseIncidents(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        assigned_team: Optional[str] = None,
        affected_service: Optional[str] = None,
        created_since: Optional[str] = None
    ) -> str:
        incidents = data.get("incidents", {})
        assignments = data.get("incident_assignments", {})
        results = []
        for rec in incidents.values():
            if status and rec.get("status") != status:
                continue
            if priority and rec.get("priority") != priority:
                continue
            if category and rec.get("category") != category:
                continue
            if affected_service and rec.get("affected_service_id") != affected_service:
                continue
            if created_since and isinstance(rec.get("created_at"), str) and rec.get("created_at") < created_since:
                continue
            if assigned_team:
                # find any active assignment for this incident with matching team
                found = False
                for a in assignments.values():
                    if a.get("incident_id") == rec.get("incident_id") and (a.get("unassigned_at") in (None, "")) and a.get("assigned_team") == assigned_team.lower():
                        found = True
                        break
                if not found:
                    continue
            results.append(rec)
        return json.dumps(results)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"browse_incidents",
                "description":"Filtered search of incidents for dashboards and reports.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "status":{"type":"string","description":"Filter by status. Allowed: open, in_progress, escalated, pending_vendor, resolved, closed"},
                        "priority":{"type":"string","description":"Filter by priority. Allowed: low, medium, high"},
                        "category":{"type":"string","description":"Filter by category. Allowed: hardware, software, security, performance, other"},
                        "assigned_team":{"type":"string","description":"Filter by assigned team. Allowed: service_desk, L1, L2, L3, facilities, change_mgmt, devops"},
                        "affected_service":{"type":"string","description":"Filter by services.service_id"},
                        "created_since":{"type":"string","description":"ISO timestamp (YYYY-MM-DD) to include incidents created on/after this"}
                    },
                    "required":[]
                }
            }
        }

