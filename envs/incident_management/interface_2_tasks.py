"""
Interface 2 Tasks - Incident Management Domain

This module contains example tasks for testing the functionality of Interface 2
in the incident management domain. These tasks demonstrate the basic operations
for creating, retrieving, and managing incidents, problems, vendor engagements,
changes, communications, monitoring events, simulations, tool usage, and audits.
"""

# NOTE:
# - IDs are strings.
# - Timestamps are ISO-8601 strings when present.
# - Enum values follow the Incident Management Policy & SOPs.


FIND_ENTITIES = {
    "task_id": "T201",
    "function": "find_entities",
    "params": {
        "entity_type": "incident",
        "filters": {"client_id": "1", "status": "open"},
        "requester_id": "1"
    }
}

LOG_EVENT_RECORD = {
    "task_id": "T202",
    "function": "log_event_record",
    "params": {
        "source": "alert_log",
        "payload_summary": "High latency observed on API gateway",
        "severity_hint": "P3",
        "recorded_by_id": "1"
    }
}

CORRELATE_EVENTS = {
    "task_id": "T203",
    "function": "correlate_events",
    "params": {
        "event_ids": ["4", "5"],
        "correlation_key": "SIG-API-LATENCY-2025",
        "link_incident_id": "2"
    }
}

REGISTER_CLIENT = {
    "task_id": "T204",
    "function": "register_client",
    "params": {
        "name": "Globex Ltd",
        "registration_number": "987654321",
        "contact_email": "itops@globex.example",
        "client_type": "mid_market",
        "contact_phone": "+12025550123",
        "address": "100 Main St, Springfield, USA"
    }
}

ADD_USER = {
    "task_id": "T205",
    "function": "add_user",
    "params": {
        "name": "John Smith",
        "email": "john.smith@globex.example",
        "role": "technical_support",
        "timezone": "America/New_York",
        "client_id": "2"
    }
}

ONBOARD_VENDOR = {
    "task_id": "T206",
    "function": "onboard_vendor",
    "params": {
        "vendor_name": "SecureFire LLC",
        "contact_email": "support@securefire.example",
        "contact_phone": "+13125550100",
        "vendor_type": "security_service"
    }
}

REGISTER_PRODUCT = {
    "task_id": "T207",
    "function": "register_product",
    "params": {
        "product_name": "BankCore",
        "product_type": "banking_system",
        "version": "10.4.0",
        "vendor_id": "2"
    }
}

REGISTER_COMPONENT = {
    "task_id": "T208",
    "function": "register_component",
    "params": {
        "product_id": "2",
        "component_name": "bankcore-lb-west",
        "component_type": "load_balancer",
        "environment": "production",
        "location": "us-west-2",
        "ports": "443,8443",
        "status": "online"
    }
}

START_SUBSCRIPTION = {
    "task_id": "T209",
    "function": "start_subscription",
    "params": {
        "client_id": "2",
        "product_id": "2",
        "subscription_type": "limited_service",
        "service_level_tier": "standard",
        "start_date": "2025-02-01",
        "end_date": None,
        "recovery_objectives": "RTO 8h / RPO 30m"
    }
}

DEFINE_SLA = {
    "task_id": "T210",
    "function": "define_sla",
    "params": {
        "subscription_id": "2",
        "severity_level": "P2",
        "response_time_minutes": 60,
        "resolution_time_hours": 12,
        "availability_target": 99.5
    }
}

OPEN_INCIDENT = {
    "task_id": "T211",
    "function": "open_incident",
    "params": {
        "reporter_id": "3",
        "client_id": "2",
        "title": "Intermittent API timeouts",
        "description": "Clients report sporadic 504s",
        "category": "api_error",
        "severity": "P3",
        "impact_level": "medium",
        "component_id": "2"
    }
}

LOG_COMMUNICATION = {
    "task_id": "T212",
    "function": "log_communication",
    "params": {
        "incident_id": "2",
        "sender_user": "3",
        "recipient": "client_contact",
        "delivery_method": "email",
        "message_content": "We are investigating API timeouts. Next update in 30 minutes."
    }
}

APPLY_WORKAROUND = {
    "task_id": "T213",
    "function": "apply_workaround",
    "params": {
        "incident_id": "2",
        "description": "Increase timeout threshold and retry policy",
        "effectiveness": "effective",
        "implemented_by": "4"
    }
}

INITIATE_RCA = {
    "task_id": "T214",
    "function": "initiate_rca",
    "params": {
        "incident_id": "2",
        "analysis_method": "fishbone_diagram",
        "assigned_to": "5"
    }
}

RAISE_ESCALATION = {
    "task_id": "T215",
    "function": "raise_escalation",
    "params": {
        "incident_id": "2",
        "target_user": "6",
        "reason": "severity_increase",
        "requested_by": "3",
        "escalation_level": "technical"
    }
}

SUBMIT_CHANGE_REQUEST = {
    "task_id": "T216",
    "function": "submit_change_request",
    "params": {
        "change_title": "Tune API gateway idle timeouts",
        "change_type": "standard",
        "risk_level": "medium",
        "requested_by": "3",
        "incident_id": "2"
    }
}

SUBMIT_ROLLBACK_REQUEST = {
    "task_id": "T217",
    "function": "submit_rollback_request",
    "params": {
        "change_id": "2",
        "justification": "New policy causes client retries to fail",
        "requested_by": "3",
        "incident_id": "2"
    }
}

LOG_METRIC = {
    "task_id": "T218",
    "function": "log_metric",
    "params": {
        "incident_id": "2",
        "metric_type": "mean_time_to_acknowledge",
        "calculated_value_minutes": 25,
        "target_minutes": 30
    }
}

PRODUCE_INCIDENT_REPORT = {
    "task_id": "T219",
    "function": "produce_incident_report",
    "params": {
        "incident_id": "2",
        "report_type": "trend_analysis",
        "generated_by": "3"
    }
}

DRAFT_KB_ARTICLE = {
    "task_id": "T220",
    "function": "draft_kb_article",
    "params": {
        "title": "API Timeout Mitigation Steps",
        "content_type": "troubleshooting",
        "category": "troubleshooting",
        "author_id": "3",
        "incident_id": "2",
        "reviewer_user_id": "6"
    }
}

SCHEDULE_POST_INCIDENT_REVIEW = {
    "task_id": "T221",
    "function": "schedule_post_incident_review",
    "params": {
        "incident_id": "2",
        "scheduled_date": "2025-11-05",
        "facilitator_user_id": "3"
    }
}

MODIFY_CLIENT = {
    "task_id": "T222",
    "function": "modify_client",
    "params": {
        "client_id": "2",
        "changes": {"status": "active", "address": "200 Broad St, Springfield"},
        "requester_id": "3"
    }
}

MODIFY_USER_PERMISSIONS = {
    "task_id": "T223",
    "function": "modify_user_permissions",
    "params": {
        "user_id": "6",
        "requested_changes": {"role": "incident_manager", "status": "active"},
        "modified_by": "3"
    }
}

MODIFY_PRODUCT = {
    "task_id": "T224",
    "function": "modify_product",
    "params": {
        "product_id": "2",
        "changes": {"version": "10.5.0", "status": "active"}
    }
}

MODIFY_COMPONENT = {
    "task_id": "T225",
    "function": "modify_component",
    "params": {
        "component_id": "2",
        "changes": {"status": "maintenance", "environment": "staging"}
    }
}

MODIFY_SUBSCRIPTION = {
    "task_id": "T226",
    "function": "modify_subscription",
    "params": {
        "subscription_id": "2",
        "changes": {"service_level_tier": "premium", "rto_hours": 6}
    }
}

MODIFY_SLA = {
    "task_id": "T227",
    "function": "modify_sla",
    "params": {
        "sla_id": "2",
        "changes": {"response_time_minutes": 45, "status": "active"}
    }
}

MODIFY_INCIDENT = {
    "task_id": "T228",
    "function": "modify_incident",
    "params": {
        "incident_id": "2",
        "new_status": "in_progress",
        "field_updates": {"assigned_manager_id": "3", "severity": "P3"},
        "updated_by": "3"
    }
}

MODIFY_ESCALATION = {
    "task_id": "T229",
    "function": "modify_escalation",
    "params": {
        "escalation_id": "2",
        "changes": {"status": "acknowledged", "acknowledged_at": "2025-10-01T01:00:00"}
    }
}

MODIFY_CHANGE_REQUEST = {
    "task_id": "T230",
    "function": "modify_change_request",
    "params": {
        "change_id": "2",
        "changes": {"status": "scheduled", "scheduled_start": "2025-10-03T03:00:00"}
    }
}

MODIFY_ROLLBACK_REQUEST = {
    "task_id": "T231",
    "function": "modify_rollback_request",
    "params": {
        "rollback_id": "2",
        "changes": {"status": "in_progress", "approved_by_id": "6"}
    }
}

MODIFY_RCA = {
    "task_id": "T232",
    "function": "modify_rca",
    "params": {
        "rca_id": "2",
        "changes": {"status": "approved", "summary": "Timeouts linked to idle connection policy"}
    }
}

MODIFY_COMMUNICATION = {
    "task_id": "T233",
    "function": "modify_communication",
    "params": {
        "communication_id": "2",
        "changes": {"delivery_status": "sent", "sent_at": "2025-10-01T00:20:00"}
    }
}

MODIFY_KB_ARTICLE = {
    "task_id": "T234",
    "function": "modify_kb_article",
    "params": {
        "article_id": "2",
        "changes": {"status": "published", "reviewer_user_id": "6"}
    }
}

MODIFY_POST_INCIDENT_REVIEW = {
    "task_id": "T235",
    "function": "modify_post_incident_review",
    "params": {
        "pir_id": "2",
        "changes": {"status": "in_progress", "scheduled_date": "2025-11-06"}
    }
}

MARK_INCIDENT_RESOLVED = {
    "task_id": "T236",
    "function": "mark_incident_resolved",
    "params": {
        "incident_id": "2",
        "resolved_by": "3",
        "resolution_summary": "Adjusted gateway settings and restored stability"
    }
}

FINALIZE_INCIDENT = {
    "task_id": "T237",
    "function": "finalize_incident",
    "params": {
        "incident_id": "2",
        "closed_by": "3"
    }
}

ASSESS_SEVERITY = {
    "task_id": "T238",
    "function": "assess_severity",
    "params": {
        "complete_outage": False,
        "client_count_impacted": 2,
        "has_workaround": True,
        "regulatory_or_financial_impact": False,
        "is_priority_client": False
    }
}

WRITE_AUDIT_TRAIL = {
    "task_id": "T239",
    "function": "write_audit_trail",
    "params": {
        "user_id": "3",
        "action": "update",
        "reference_type": "incident",
        "reference_id": "2",
        "field_name": "status",
        "old_value": "in_progress",
        "new_value": "resolved"
    }
}

ESCALATE_TO_HUMAN = {
    "task_id": "T240",
    "function": "escalate_to_human",
    "params": {
        "reason_code": "policy_exception",
        "details": "Vendor approval missing for emergency change"
    }
}

FETCH_INCIDENT = {
    "task_id": "T241",
    "function": "fetch_incident",
    "params": {
        "incident_id": "2"
    }
}

FETCH_EVENT_RECORDS = {
    "task_id": "T242",
    "function": "fetch_event_records",
    "params": {
        "source": "alert_log",
        "severity_hint": "P3"
    }
}

FETCH_ESCALATIONS = {
    "task_id": "T243",
    "function": "fetch_escalations",
    "params": {
        "incident_id": "2",
        "status": "acknowledged"
    }
}

FETCH_COMMUNICATIONS = {
    "task_id": "T244",
    "function": "fetch_communications",
    "params": {
        "incident_id": "2",
        "delivery_status": "sent"
    }
}

FETCH_KB_ARTICLES = {
    "task_id": "T245",
    "function": "fetch_kb_articles",
    "params": {
        "category": "troubleshooting",
        "status": "published"
    }
}

VERIFY_APPROVAL = {
    "task_id": "T246",
    "function": "verify_approval",
    "params": {
        "reference_type": "change_request",
        "reference_id": "2",
        "requested_action": "schedule",
        "approver_id": "6"
    }
}

INTERFACE_2_TASKS = [
    FIND_ENTITIES,
    LOG_EVENT_RECORD,
    CORRELATE_EVENTS,
    REGISTER_CLIENT,
    ADD_USER,
    ONBOARD_VENDOR,
    REGISTER_PRODUCT,
    REGISTER_COMPONENT,
    START_SUBSCRIPTION,
    DEFINE_SLA,
    OPEN_INCIDENT,
    LOG_COMMUNICATION,
    APPLY_WORKAROUND,
    INITIATE_RCA,
    RAISE_ESCALATION,
    SUBMIT_CHANGE_REQUEST,
    SUBMIT_ROLLBACK_REQUEST,
    LOG_METRIC,
    PRODUCE_INCIDENT_REPORT,
    DRAFT_KB_ARTICLE,
    SCHEDULE_POST_INCIDENT_REVIEW,
    MODIFY_CLIENT,
    MODIFY_USER_PERMISSIONS,
    MODIFY_PRODUCT,
    MODIFY_COMPONENT,
    MODIFY_SUBSCRIPTION,
    MODIFY_SLA,
    MODIFY_INCIDENT,
    MODIFY_ESCALATION,
    MODIFY_CHANGE_REQUEST,
    MODIFY_ROLLBACK_REQUEST,
    MODIFY_RCA,
    MODIFY_COMMUNICATION,
    MODIFY_KB_ARTICLE,
    MODIFY_POST_INCIDENT_REVIEW,
    MARK_INCIDENT_RESOLVED,
    FINALIZE_INCIDENT,
    ASSESS_SEVERITY,
    WRITE_AUDIT_TRAIL,
    ESCALATE_TO_HUMAN,
    FETCH_INCIDENT,
    FETCH_EVENT_RECORDS,
    FETCH_ESCALATIONS,
    FETCH_COMMUNICATIONS,
    FETCH_KB_ARTICLES,
    VERIFY_APPROVAL,
]


def get_task_by_id(task_id):
    """Get a specific task by its ID"""
    for task in INTERFACE_2_TASKS:
        if task["task_id"] == task_id:
            return task
    return None


def get_tasks_by_function(function_name):
    """Get all tasks for a specific function"""
    return [task for task in INTERFACE_2_TASKS if task["function"] == function_name]


def get_all_tasks():
    """Get all tasks for Interface 2"""
    return INTERFACE_2_TASKS


def get_task_count():
    """Get the total number of tasks"""
    return len(INTERFACE_2_TASKS)
