
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


class RegisterComponent(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any],
               product_id: str,
               component_name: str,
               component_type: str,
               environment: str,
               location: Optional[str] = None,
               ports: Optional[str] = None,
               status: str = "online") -> str:
        products   = data.get("products", {})
        components = data.get("components", {})

        allowed_ct = ["sftp_server","api_endpoint","database","load_balancer","firewall","authentication_service","payment_gateway","file_storage","monitoring_system"]
        allowed_env= ["production","staging","development","test"]
        allowed_st = ["online","offline","maintenance","degraded"]

        if not _ensure_exists(products, product_id):
            return json.dumps({"error":"product_id not found"})
        if not component_name or not component_type or not environment:
            return json.dumps({"error":"component_name, component_type, environment are required"})

        if component_type not in allowed_ct:
            return json.dumps({"error":"Invalid component_type. Allowed: " + "|".join(allowed_ct)})
        if environment not in allowed_env:
            return json.dumps({"error":"Invalid environment. Allowed: production|staging|development|test"})
        if status not in allowed_st:
            return json.dumps({"error":"Invalid status. Allowed: online|offline|maintenance|degraded"})

        comp_id = _generate_id(components)
        row = {
            "component_id": comp_id,
            "product_id": product_id,
            "name": component_name,
            "component_type": component_type,
            "environment": environment,
            "location": location,
            "port_number": None if ports is None else ports,
            "status": status,
            "created_at": TS,
            "updated_at": TS
        }
        components[comp_id] = row
        return json.dumps(row)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_component",
                "description": "Register an infrastructure component under a product.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "Product ID (required)"
                        },
                        "component_name": {
                            "type": "string",
                            "description": "Component name (required)"
                        },
                        "component_type": {
                            "type": "string",
                            "description": "Enum: sftp_server|api_endpoint|database|load_balancer|firewall|authentication_service|payment_gateway|file_storage|monitoring_system"
                        },
                        "environment": {
                            "type": "string",
                            "description": "Enum: production|staging|development|test"
                        },
                        "location": {
                            "type": "string",
                            "description": "Optional location"
                        },
                        "ports": {
                            "type": "string",
                            "description": "Optional port(s) string"
                        },
                        "status": {
                            "type": "string",
                            "description": "Optional. Enum: online|offline|maintenance|degraded"
                        }
                    },
                    # <-- status is OPTIONAL now (removed from required)
                    "required": ["product_id", "component_name", "component_type", "environment"]
                }
            }
        }