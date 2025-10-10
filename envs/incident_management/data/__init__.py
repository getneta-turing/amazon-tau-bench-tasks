
import json
import os
from typing import Dict, Any

# List of all JSON files that make up the HR Payroll / Payment domain
DATA_FILES = [
    "approvals.json",
    "audit_trails.json",
    "change_requests.json",
    "clients.json",
    "communications.json",
    "components.json",
    "escalations.json",
    "event_correlations.json",
    "event_records.json",
    "incident_reports.json",
    "incidents.json",
    "knowledge_base_articles.json",
    "metrics.json",
    "post_incident_reviews.json",
    "products.json",
    "rollback_requests.json",
    "root_cause_analyses.json",
    "sla_agreements.json",
    "subscriptions.json",
    "users.json",
    "vendors.json",
    "workarounds.json",
]

def load_data(base_dir: str = None) -> Dict[str, Any]:
    """
    Load all seeded JSON data for the payroll_management domain.

    Args:
        base_dir: optional override path. Defaults to this package directory.

    Returns:
        Dict mapping table_name (without .json) -> dict-of-records
    """
    if base_dir is None:
        base_dir = os.path.dirname(__file__)

    data = {}
    for filename in DATA_FILES:
        path = os.path.join(base_dir, filename)
        table_name = filename.replace(".json", "")
        with open(path, "r", encoding="utf-8") as f:
            data[table_name] = json.load(f)
    return data