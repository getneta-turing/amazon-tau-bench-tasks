import json
from typing import Any, Dict
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
class DocumentIncidentSimulation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        scenario_name: str,
        simulated_by_user_id: str,
        scope: str
    ) -> str:
        users = data.get("users", {})
        if str(simulated_by_user_id) not in users:
            return json.dumps({"error": f"User {simulated_by_user_id} not found"})

        sims = data.setdefault("simulations", {})
        sid = _generate_id(sims)
        rec = {
            "simulation_id": str(sid),
            "scenario_name": scenario_name,
            "simulated_by_user_id": str(simulated_by_user_id),
            "scope": scope,
            "started_at": TIMESTAMP,
            "ended_at": None,
            "outcome": "completed",
            "notes": None
        }
        sims[str(sid)] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str,Any]:
        return {
            "type":"function",
            "function":{
                "name":"document_incident_simulation",
                "description":"Record a simulation/test drill walkthrough and outcomes.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "scenario_name":{"type":"string","description":"Name of the scenario"},
                        "simulated_by_user_id":{"type":"string","description":"User ID (Incident Manager) who simulated"},
                        "scope":{"type":"string","description":"Service/system scope"}
                    },
                    "required":["scenario_name","simulated_by_user_id","scope"]
                }
            }
        }
