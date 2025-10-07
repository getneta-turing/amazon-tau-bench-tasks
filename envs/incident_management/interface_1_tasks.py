"""
Interface 1 Tasks - Incident Management Domain

This module contains example tasks for testing the functionality of Interface 1
in the incident management domain. These tasks demonstrate the basic operations
for creating, retrieving, and managing incidents, problems, vendor engagements,
changes, communications, monitoring events, simulations, tool usage, and audits.
"""

# NOTE:
# - IDs are strings.
# - Timestamps are ISO-8601 strings when present.
# - Enum values follow the Incident Management Policy & SOPs.


DISCOVER_ENTITIES = {
    "task_id": "T001",
    "function": "discover_entities",
    "params": {
        "entity_type": "incident",
        "filters": {"client_id": "1", "status": "open"},
        "requester_id": "1"
    }
}

CREATE_EVENT_RECORD = {
    "task_id": "T002",
    "function": "create_event_record",
    "params": {
        "source": "alert_log",
        "payload_summary": "Database connection timeout spikes detected",
        "severity_hint": "P2",
        "recorded_by_id": "1"
    }
}

CORRELATE_EVENTS_ONCE = {
    "task_id": "T003",
    "function": "correlate_events_once",
    "params": {
        "event_ids": ["1", "2", "3"],
        "correlation_key": "SIG-DB-TIMEOUT-2025",
        "link_incident_id": "1"
    }
}

CREATE_CLIENT = {
    "task_id": "T004",
    "function": "create_client",
    "params": {
        "name": "Acme Corp LLC",
        "registration_number": "123456789",
        "contact_email": "ops@acme.example",
        "client_type": "enterprise",
        "contact_phone": "+14155550123",
        "address": "1 Market St, San Francisco, CA 94105"
    }
}

CREATE_USER = {
    "task_id": "T005",
    "function": "create_user",
    "params": {
        "name": "Jane Doe",
        "email": "jane.doe@acme.example",
        "role": "incident_manager",
        "timezone": "America/Los_Angeles",
        "client_id": "1"
    }
}

REGISTER_VENDOR = {
    "task_id": "T006",
    "function": "register_vendor",
    "params": {
        "vendor_name": "CloudyOps Inc",
        "contact_email": "support@cloudyops.example",
        "contact_phone": "+12125550100",
        "vendor_type": "cloud_service_provider"
    }
}

CREATE_PRODUCT = {
    "task_id": "T007",
    "function": "create_product",
    "params": {
        "product_name": "Payment Gateway X",
        "product_type": "payment_processing",
        "version": "3.2.1",
        "vendor_id": "1"
    }
}

CREATE_COMPONENT = {
    "task_id": "T008",
    "function": "create_component",
    "params": {
        "product_id": "1",
        "component_name": "pgx-db-east-1",
        "component_type": "database",
        "environment": "production",
        "location": "us-east-1",
        "ports": "5432",
        "status": "online"
    }
}

CREATE_SUBSCRIPTION = {
    "task_id": "T009",
    "function": "create_subscription",
    "params": {
        "client_id": "1",
        "product_id": "1",
        "subscription_type": "full_service",
        "service_level_tier": "premium",
        "start_date": "2025-01-01",
        "end_date": None,
        "recovery_objectives": "RTO 4h / RPO 15m"
    }
}

CREATE_SLA = {
    "task_id": "T010",
    "function": "create_sla",
    "params": {
        "subscription_id": "1",
        "severity_level": "P1",
        "response_time_minutes": 30,
        "resolution_time_hours": 8,
        "availability_target": 99.9
    }
}

CREATE_INCIDENT = {
    "task_id": "T011",
    "function": "create_incident",
    "params": {
        "reporter_id": "2",
        "client_id": "1",
        "title": "Gateway DB connection timeouts",
        "description": "Spike in timeouts observed from multiple AZs",
        "category": "database_issue",
        "severity": "P2",
        "impact_level": "high",
        "component_id": "1"
    }
}

RECORD_COMMUNICATION = {
    "task_id": "T012",
    "function": "record_communication",
    "params": {
        "incident_id": "1",
        "sender_user": "2",
        "recipient": "executive_team",
        "delivery_method": "incident_portal_update",
        "message_content": "Incident declared. Team engaged. Next update in 30m."
    }
}

IMPLEMENT_WORKAROUND = {
    "task_id": "T013",
    "function": "implement_workaround",
    "params": {
        "incident_id": "1",
        "description": "Increase DB connection pool and throttle retries",
        "effectiveness": "partially_effective",
        "implemented_by": "3"
    }
}

START_RCA = {
    "task_id": "T014",
    "function": "start_rca",
    "params": {
        "incident_id": "1",
        "analysis_method": "five_whys",
        "assigned_to": "4"
    }
}

CREATE_ESCALATION = {
    "task_id": "T015",
    "function": "create_escalation",
    "params": {
        "incident_id": "1",
        "target_user": "5",
        "reason": "sla_breach",
        "requested_by": "2",
        "escalation_level": "management"
    }
}

CREATE_CHANGE_REQUEST = {
    "task_id": "T016",
    "function": "create_change_request",
    "params": {
        "change_title": "Add read replicas & tune timeouts",
        "change_type": "normal",
        "risk_level": "high",
        "requested_by": "2",
        "incident_id": "1"
    }
}

CREATE_ROLLBACK_REQUEST = {
    "task_id": "T017",
    "function": "create_rollback_request",
    "params": {
        "change_id": "1",
        "justification": "Performance regression after change",
        "requested_by": "2",
        "incident_id": "1"
    }
}

RECORD_METRIC = {
    "task_id": "T018",
    "function": "record_metric",
    "params": {
        "incident_id": "1",
        "metric_type": "mean_time_to_resolve",
        "calculated_value_minutes": 720,
        "target_minutes": 480
    }
}

GENERATE_INCIDENT_REPORT = {
    "task_id": "T019",
    "function": "generate_incident_report",
    "params": {
        "incident_id": "1",
        "report_type": "executive_summary",
        "generated_by": "2"
    }
}

CREATE_KB_ARTICLE = {
    "task_id": "T020",
    "function": "create_kb_article",
    "params": {
        "title": "DB Timeout Tuning Guide",
        "content_type": "resolution_steps",
        "category": "incident_resolution",
        "author_id": "2",
        "incident_id": "1",
        "reviewer_user_id": "5"
    }
}

CREATE_POST_INCIDENT_REVIEW = {
    "task_id": "T021",
    "function": "create_post_incident_review",
    "params": {
        "incident_id": "1",
        "scheduled_date": "2025-10-10",
        "facilitator_user_id": "2"
    }
}

UPDATE_CLIENT = {
    "task_id": "T022",
    "function": "update_client",
    "params": {
        "client_id": "1",
        "changes": {"status": "active", "address": "2 Ocean Ave, SF, CA"},
        "requester_id": "2"
    }
}

UPDATE_USER_PERMISSIONS = {
    "task_id": "T023",
    "function": "update_user_permissions",
    "params": {
        "user_id": "5",
        "requested_changes": {"role": "technical_support", "status": "active"},
        "modified_by": "2"
    }
}

UPDATE_PRODUCT = {
    "task_id": "T024",
    "function": "update_product",
    "params": {
        "product_id": "1",
        "changes": {"version": "3.3.0", "status": "active"}
    }
}

UPDATE_COMPONENT = {
    "task_id": "T025",
    "function": "update_component",
    "params": {
        "component_id": "1",
        "changes": {"status": "maintenance", "environment": "staging"}
    }
}

UPDATE_SUBSCRIPTION = {
    "task_id": "T026",
    "function": "update_subscription",
    "params": {
        "subscription_id": "1",
        "changes": {"service_level_tier": "standard", "rto_hours": 8}
    }
}

UPDATE_SLA = {
    "task_id": "T027",
    "function": "update_sla",
    "params": {
        "sla_id": "1",
        "changes": {"response_time_minutes": 20, "status": "active"}
    }
}

UPDATE_INCIDENT = {
    "task_id": "T028",
    "function": "update_incident",
    "params": {
        "incident_id": "1",
        "new_status": "in_progress",
        "field_updates": {"assigned_manager_id": "2", "severity": "P2"},
        "updated_by": "2"
    }
}

UPDATE_ESCALATION = {
    "task_id": "T029",
    "function": "update_escalation",
    "params": {
        "escalation_id": "1",
        "changes": {"status": "acknowledged", "acknowledged_at": "2025-10-01T00:30:00"}
    }
}

UPDATE_CHANGE_REQUEST = {
    "task_id": "T030",
    "function": "update_change_request",
    "params": {
        "change_id": "1",
        "changes": {"status": "scheduled", "scheduled_start": "2025-10-02T02:00:00"}
    }
}

UPDATE_ROLLBACK_REQUEST = {
    "task_id": "T031",
    "function": "update_rollback_request",
    "params": {
        "rollback_id": "1",
        "changes": {"status": "approved", "approved_by_id": "5"}
    }
}

UPDATE_RCA = {
    "task_id": "T032",
    "function": "update_rca",
    "params": {
        "rca_id": "1",
        "changes": {"status": "completed", "summary": "Connection pool exhaustion"}
    }
}

UPDATE_COMMUNICATION = {
    "task_id": "T033",
    "function": "update_communication",
    "params": {
        "communication_id": "1",
        "changes": {"delivery_status": "delivered", "sent_at": "2025-10-01T00:10:00"}
    }
}

UPDATE_KB_ARTICLE = {
    "task_id": "T034",
    "function": "update_kb_article",
    "params": {
        "article_id": "1",
        "changes": {"status": "published", "reviewer_user_id": "5"}
    }
}

UPDATE_POST_INCIDENT_REVIEW = {
    "task_id": "T035",
    "function": "update_post_incident_review",
    "params": {
        "pir_id": "1",
        "changes": {"status": "in_progress", "scheduled_date": "2025-10-11"}
    }
}

RESOLVE_INCIDENT = {
    "task_id": "T036",
    "function": "resolve_incident",
    "params": {
        "incident_id": "1",
        "resolved_by": "2",
        "resolution_summary": "Scaled DB cluster and tuned connection pooling"
    }
}

CLOSE_INCIDENT = {
    "task_id": "T037",
    "function": "close_incident",
    "params": {
        "incident_id": "1",
        "closed_by": "2"
    }
}

LOG_AUDIT_TRAIL = {
    "task_id": "T038",
    "function": "log_audit_trail",
    "params": {
        "user_id": "2",
        "action": "update",
        "reference_type": "incident",
        "reference_id": "1",
        "field_name": "status",
        "old_value": "in_progress",
        "new_value": "resolved"
    }
}

TRANSFER_TO_HUMAN = {
    "task_id": "T039",
    "function": "transfer_to_human",
    "params": {
        "reason_code": "approval_missing",
        "details": "Change requires executive approval"
    }
}

GET_INCIDENT = {
    "task_id": "T040",
    "function": "get_incident",
    "params": {
        "incident_id": "1"
    }
}

GET_EVENT_RECORDS = {
    "task_id": "T041",
    "function": "get_event_records",
    "params": {
        "source": "alert_log",
        "severity_hint": "P2"
    }
}

GET_ESCALATIONS = {
    "task_id": "T042",
    "function": "get_escalations",
    "params": {
        "incident_id": "1",
        "status": "acknowledged"
    }
}

GET_COMMUNICATIONS = {
    "task_id": "T043",
    "function": "get_communications",
    "params": {
        "incident_id": "1",
        "delivery_status": "delivered"
    }
}

GET_KB_ARTICLES = {
    "task_id": "T044",
    "function": "get_kb_articles",
    "params": {
        "category": "incident_resolution",
        "status": "published"
    }
}

CLASSIFY_SEVERITY = {
    "task_id": "T045",
    "function": "classify_severity",
    "params": {
        "complete_outage": False,
        "client_count_impacted": 3,
        "has_workaround": True,
        "regulatory_or_financial_impact": False,
        "is_priority_client": True
    }
}

CHECK_APPROVAL = {
    "task_id": "T046",
    "function": "check_approval",
    "params": {
        "reference_type": "change_request",
        "reference_id": "1",
        "requested_action": "schedule",
        "approver_id": "5"
    }
}

INTERFACE_1_TASKS = [
    DISCOVER_ENTITIES,
    CREATE_EVENT_RECORD,
    CORRELATE_EVENTS_ONCE,
    CREATE_CLIENT,
    CREATE_USER,
    REGISTER_VENDOR,
    CREATE_PRODUCT,
    CREATE_COMPONENT,
    CREATE_SUBSCRIPTION,
    CREATE_SLA,
    CREATE_INCIDENT,
    RECORD_COMMUNICATION,
    IMPLEMENT_WORKAROUND,
    START_RCA,
    CREATE_ESCALATION,
    CREATE_CHANGE_REQUEST,
    CREATE_ROLLBACK_REQUEST,
    RECORD_METRIC,
    GENERATE_INCIDENT_REPORT,
    CREATE_KB_ARTICLE,
    CREATE_POST_INCIDENT_REVIEW,
    UPDATE_CLIENT,
    UPDATE_USER_PERMISSIONS,
    UPDATE_PRODUCT,
    UPDATE_COMPONENT,
    UPDATE_SUBSCRIPTION,
    UPDATE_SLA,
    UPDATE_INCIDENT,
    UPDATE_ESCALATION,
    UPDATE_CHANGE_REQUEST,
    UPDATE_ROLLBACK_REQUEST,
    UPDATE_RCA,
    UPDATE_COMMUNICATION,
    UPDATE_KB_ARTICLE,
    UPDATE_POST_INCIDENT_REVIEW,
    RESOLVE_INCIDENT,
    CLOSE_INCIDENT,
    LOG_AUDIT_TRAIL,
    TRANSFER_TO_HUMAN,
    GET_INCIDENT,
    GET_EVENT_RECORDS,
    GET_ESCALATIONS,
    GET_COMMUNICATIONS,
    GET_KB_ARTICLES,
    CLASSIFY_SEVERITY,
    CHECK_APPROVAL,
]


def get_task_by_id(task_id):
    """Get a specific task by its ID"""
    for task in INTERFACE_1_TASKS:
        if task["task_id"] == task_id:
            return task
    return None


def get_tasks_by_function(function_name):
    """Get all tasks for a specific function"""
    return [task for task in INTERFACE_1_TASKS if task["function"] == function_name]


def get_all_tasks():
    """Get all tasks for Interface 1"""
    return INTERFACE_1_TASKS


def get_task_count():
    """Get the total number of tasks"""
    return len(INTERFACE_1_TASKS)
