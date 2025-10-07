
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


def _ensure_exists(table: Dict[str, Any], key: Optional[str]) -> bool:
    if key is None:
        return False
    return str(key) in table


class FileIncident(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               reporter_id: str,
               client_id: str,
               title: str,
               description: str,
               category: str,
               severity: str,
               impact_level: str,
               component_id: Optional[str] = None) -> str:
        users = data.get("users", {})
        clients = data.get("clients", {})
        components = data.get("components", {})
        incidents = data.get("incidents", {})

        cats = ["system_outage","performance_degradation","security_incident","data_corruption","integration_failure","network_issue","hardware_failure","software_bug","configuration_error","capacity_issue","backup_failure","authentication_failure","api_error","database_issue","service_unavailable"]
        sev = ["P1","P2","P3","P4"]
        imp = ["critical","high","medium","low"]

        if not _ensure_exists(users, reporter_id):
            return json.dumps({"error":"reporter_id not found"})
        if not _ensure_exists(clients, client_id):
            return json.dumps({"error":"client_id not found"})
        if component_id is not None and not _ensure_exists(components, component_id):
            return json.dumps({"error":"component_id not found"})

        if category not in cats:
            return json.dumps({"error":"Invalid category"})
        if severity not in sev:
            return json.dumps({"error":"Invalid severity (P1|P2|P3|P4)"})
        if impact_level not in imp:
            return json.dumps({"error":"Invalid impact_level (critical|high|medium|low)"})
        if not title or not description:
            return json.dumps({"error":"title and description are required"})

        iid = _generate_id(incidents)
        row = {
            "incident_id": iid,
            "incident_code": f"INC-{iid.zfill(8)}",
            "client_id": client_id,
            "component_id": component_id,
            "reporter_id": reporter_id,
            "assigned_manager_id": None,
            "title": title,
            "description": description,
            "category": category,
            "severity": severity,
            "impact": impact_level,
            "urgency": impact_level,
            "status": "open",
            "detection_source": "client_reported",
            "is_recurring": False,
            "downtime_minutes": 0,
            "sla_breach": False,
            "rto_breach": False,
            "detected_at": TS,
            "resolved_at": None,
            "closed_at": None,
            "created_at": TS,
            "updated_at": TS
        }
        incidents[iid] = row
        return json.dumps(row)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"file_incident",
                "description":"Formally log an incident.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "reporter_id":{"type":"string","description":"User ID (required)"},
                        "client_id":{"type":"string","description":"Client ID (required)"},
                        "title":{"type":"string","description":"Title (required)"},
                        "description":{"type":"string","description":"Description (required)"},
                        "category":{"type":"string","description":"Required policy category"},
                        "severity":{"type":"string","description":"Required: P1|P2|P3|P4"},
                        "impact_level":{"type":"string","description":"Required: critical|high|medium|low"},
                        "component_id":{"type":"string","description":"Optional component id"}
                    },
                    "required":["reporter_id","client_id","title","description","category","severity","impact_level"]
                }
            }
        }
