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
class OpenVendorCase(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        incident_id: str,
        vendor_name: str,
        contact_method: str,
        initiated_by_user_id: str,
        vendor_ticket_reference: Optional[str] = None
    ) -> str:
        incidents = data.get("incidents", {})
        users = data.get("users", {})
        if str(incident_id) not in incidents:
            return json.dumps({"error": f"Incident {incident_id} not found"})
        if str(initiated_by_user_id) not in users:
            return json.dumps({"error": f"User {initiated_by_user_id} not found"})
        allowed = ["phone","email","vendor_portal","API"]
        if contact_method not in allowed:
            return json.dumps({"error": f"Invalid contact_method. Allowed: {allowed}"})

        ve = data.setdefault("vendor_engagements", {})
        vid = _generate_id(ve)
        ve[str(vid)] = {
            "vendor_engagement_id": str(vid),
            "incident_id": str(incident_id),
            "vendor_name": vendor_name,
            "contact_method": contact_method,
            "vendor_ticket_reference": vendor_ticket_reference,
            "status": "pending_vendor",
            "initiated_by_user_id": str(initiated_by_user_id),
            "created_at": TIMESTAMP,
            "updated_at": TIMESTAMP
        }

        # update incident status
        inc = incidents[str(incident_id)]
        inc["status"] = "pending_vendor"
        incidents[str(incident_id)] = inc
        return json.dumps(ve[str(vid)])

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"open_vendor_case",
                "description":"Represent third-party vendor involvement; mark incident as pending_vendor.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "incident_id":{"type":"string","description":"Incident ID"},
                        "vendor_name":{"type":"string","description":"Vendor name"},
                        "contact_method":{"type":"string","description":"Allowed: phone, email, vendor_portal, API"},
                        "vendor_ticket_reference":{"type":"string","description":"Optional vendor ticket reference"},
                        "initiated_by_user_id":{"type":"string","description":"User ID who initiated vendor engagement"}
                    },
                    "required":["incident_id","vendor_name","contact_method","initiated_by_user_id"]
                }
            }
        }
