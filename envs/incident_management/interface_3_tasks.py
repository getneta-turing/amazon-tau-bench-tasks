"""
Interface 3 Tasks - Incident Management Domain 

This module contains example tasks for testing the functionality of Interface 3
in the incident management domain. These tasks demonstrate the basic operations
for creating, retrieving, and managing incidents, problems, vendor engagements,
changes, communications, monitoring events, simulations, tool usage, and audits.
"""

# NOTE:
# - IDs are strings.
# - Timestamps are ISO-8601 strings when present.
# - Enum values follow the Incident Management Policy & SOPs.


# 1) locate_entities (GET)
LOCATE_ENTITIES = {
    "task_id": "T301",
    "function": "locate_entities",
    "params": {
        "entity_type": "incident",
        "filters": {"client_id": "1", "status": "open"},
        "requester_id": "1"
    }
}

# 2) append_event_record (SET)
APPEND_EVENT_RECORD = {
    "task_id": "T302",
    "function": "append_event_record",
    "params": {
        "source": "alert_log",
        "payload_summary": "Disk latency spike on database node",
        "severity_hint": "P2",
        "recorded_by_id": "1"
    }
}

# 3) link_events_once (SET)
LINK_EVENTS_ONCE = {
    "task_id": "T303",
    "function": "link_events_once",
    "params": {
        "event_ids": ["7", "8"],
        "correlation_key": "SIG-DB-LAT-2025",
        "link_incident_id": "3"
    }
}

# 4) enroll_client (SET)
ENROLL_CLIENT = {
    "task_id": "T304",
    "function": "enroll_client",
    "params": {
        "name": "Initech GmbH",
        "registration_number": "123123123",
        "contact_email": "ops@initech.example",
        "client_type": "enterprise",
        "contact_phone": "+12025550199",
        "address": "7 Factory Way, Berlin DE"
    }
}

# 5) enlist_user (SET)
ENLIST_USER = {
    "task_id": "T305",
    "function": "enlist_user",
    "params": {
        "name": "Ava Johnson",
        "email": "ava.johnson@initech.example",
        "role": "technical_support",
        "timezone": "Europe/Berlin",
        "client_id": "3"
    }
}

# 6) enroll_vendor (SET)
ENROLL_VENDOR = {
    "task_id": "T306",
    "function": "enroll_vendor",
    "params": {
        "vendor_name": "CloudArc Partners",
        "contact_email": "support@cloudarc.example",
        "contact_phone": "+13125550900",
        "vendor_type": "cloud_service_provider"
    }
}

# 7) catalog_product (SET)
CATALOG_PRODUCT = {
    "task_id": "T307",
    "function": "catalog_product",
    "params": {
        "product_name": "DataBridge",
        "product_type": "data_integration",
        "version": "4.2.1",
        "vendor_id": "3"
    }
}

# 8) catalog_component (SET)
CATALOG_COMPONENT = {
    "task_id": "T308",
    "function": "catalog_component",
    "params": {
        "product_id": "3",
        "component_name": "databridge-api-eu",
        "component_type": "api_endpoint",
        "environment": "production",
        "location": "eu-central-1",
        "ports": "443",
        "status": "online"
    }
}

# 9) initiate_subscription (SET)
INITIATE_SUBSCRIPTION = {
    "task_id": "T309",
    "function": "initiate_subscription",
    "params": {
        "client_id": "3",
        "product_id": "3",
        "subscription_type": "full_service",
        "service_level_tier": "premium",
        "start_date": "2025-03-01",
        "end_date": None,
        "recovery_objectives": "RTO 4h / RPO 15m"
    }
}

# 10) establish_sla (SET)
ESTABLISH_SLA = {
    "task_id": "T310",
    "function": "establish_sla",
    "params": {
        "subscription_id": "3",
        "severity_level": "P1",
        "response_time_minutes": 30,
        "resolution_time_hours": 8,
        "availability_target": 99.9
    }
}

# 11) file_incident (SET)
FILE_INCIDENT = {
    "task_id": "T311",
    "function": "file_incident",
    "params": {
        "reporter_id": "5",
        "client_id": "3",
        "title": "Database connection saturation",
        "description": "Pool exhaustion under peak load",
        "category": "database_issue",
        "severity": "P2",
        "impact_level": "high",
        "component_id": "3"
    }
}

# 12) capture_communication (SET)
CAPTURE_COMMUNICATION = {
    "task_id": "T312",
    "function": "capture_communication",
    "params": {
        "incident_id": "3",
        "sender_user": "5",
        "recipient": "client_contact",
        "delivery_method": "email",
        "message_content": "We are scaling DB nodes. Next update in 20 minutes."
    }
}

# 13) deploy_workaround (SET)
DEPLOY_WORKAROUND = {
    "task_id": "T313",
    "function": "deploy_workaround",
    "params": {
        "incident_id": "3",
        "description": "Increase pool size and enable circuit breaker",
        "effectiveness": "partially_effective",
        "implemented_by": "5"
    }
}

# 14) launch_rca (SET)
LAUNCH_RCA = {
    "task_id": "T314",
    "function": "launch_rca",
    "params": {
        "incident_id": "3",
        "analysis_method": "five_whys",
        "assigned_to": "6"
    }
}

# 15) initiate_escalation (SET)
INITIATE_ESCALATION = {
    "task_id": "T315",
    "function": "initiate_escalation",
    "params": {
        "incident_id": "3",
        "target_user": "7",
        "reason": "severity_increase",
        "requested_by": "5",
        "escalation_level": "management"
    }
}

# 16) raise_change_request (SET)
RAISE_CHANGE_REQUEST = {
    "task_id": "T316",
    "function": "raise_change_request",
    "params": {
        "change_title": "Increase DB connection limits and add autoscaling",
        "change_type": "standard",
        "risk_level": "high",
        "requested_by": "5",
        "incident_id": "3"
    }
}

# 17) request_rollback (SET)
REQUEST_ROLLBACK = {
    "task_id": "T317",
    "function": "request_rollback",
    "params": {
        "change_id": "3",
        "justification": "New settings cause lock contention",
        "requested_by": "5",
        "incident_id": "3"
    }
}

# 18) capture_metric (SET)
CAPTURE_METRIC = {
    "task_id": "T318",
    "function": "capture_metric",
    "params": {
        "incident_id": "3",
        "metric_type": "mean_time_to_detect",
        "calculated_value_minutes": 12,
        "target_minutes": 15
    }
}

# 19) compose_incident_report (SET)
COMPOSE_INCIDENT_REPORT = {
    "task_id": "T319",
    "function": "compose_incident_report",
    "params": {
        "incident_id": "3",
        "report_type": "executive_summary",
        "generated_by": "5"
    }
}

# 20) author_kb_article (SET)
AUTHOR_KB_ARTICLE = {
    "task_id": "T320",
    "function": "author_kb_article",
    "params": {
        "title": "DB Connection Saturation Playbook",
        "content_type": "resolution_steps",
        "category": "incident_resolution",
        "author_id": "5",
        "incident_id": "3",
        "reviewer_user_id": "7"
    }
}

# 21) arrange_post_incident_review (SET)
ARRANGE_POST_INCIDENT_REVIEW = {
    "task_id": "T321",
    "function": "arrange_post_incident_review",
    "params": {
        "incident_id": "3",
        "scheduled_date": "2025-12-10",
        "facilitator_user_id": "5"
    }
}

# 22) amend_client (SET - update)
AMEND_CLIENT = {
    "task_id": "T322",
    "function": "amend_client",
    "params": {
        "client_id": "3",
        "changes": {"status": "active", "address": "8 Factory Way, Berlin"},
        "requester_id": "5"
    }
}

# 23) amend_user_permissions (SET - update)
AMEND_USER_PERMISSIONS = {
    "task_id": "T323",
    "function": "amend_user_permissions",
    "params": {
        "user_id": "7",
        "requested_changes": {"role": "incident_manager", "status": "active"},
        "modified_by": "5"
    }
}

# 24) amend_product (SET - update)
AMEND_PRODUCT = {
    "task_id": "T324",
    "function": "amend_product",
    "params": {
        "product_id": "3",
        "changes": {"version": "4.2.2", "status": "active"}
    }
}

# 25) amend_component (SET - update)
AMEND_COMPONENT = {
    "task_id": "T325",
    "function": "amend_component",
    "params": {
        "component_id": "3",
        "changes": {"status": "maintenance", "environment": "staging"}
    }
}

# 26) amend_subscription (SET - update)
AMEND_SUBSCRIPTION = {
    "task_id": "T326",
    "function": "amend_subscription",
    "params": {
        "subscription_id": "3",
        "changes": {"service_level_tier": "premium", "rto_hours": 4}
    }
}

# 27) amend_sla (SET - update)
AMEND_SLA = {
    "task_id": "T327",
    "function": "amend_sla",
    "params": {
        "sla_id": "3",
        "changes": {"response_time_minutes": 20, "status": "active"}
    }
}

# 28) amend_incident (SET - update)
AMEND_INCIDENT = {
    "task_id": "T328",
    "function": "amend_incident",
    "params": {
        "incident_id": "3",
        "new_status": "in_progress",
        "field_updates": {"assigned_manager_id": "5", "severity": "P2"},
        "updated_by": "5"
    }
}

# 29) amend_escalation (SET - update)
AMEND_ESCALATION = {
    "task_id": "T329",
    "function": "amend_escalation",
    "params": {
        "escalation_id": "3",
        "changes": {"status": "acknowledged", "acknowledged_at": "2025-10-02T01:10:00"}
    }
}

# 30) amend_change_request (SET - update)
AMEND_CHANGE_REQUEST = {
    "task_id": "T330",
    "function": "amend_change_request",
    "params": {
        "change_id": "3",
        "changes": {"status": "scheduled", "scheduled_start": "2025-10-05T02:00:00"}
    }
}

# 31) amend_rollback_request (SET - update)
AMEND_ROLLBACK_REQUEST = {
    "task_id": "T331",
    "function": "amend_rollback_request",
    "params": {
        "rollback_id": "3",
        "changes": {"status": "in_progress", "approved_by_id": "7"}
    }
}

# 32) amend_rca (SET - update)
AMEND_RCA = {
    "task_id": "T332",
    "function": "amend_rca",
    "params": {
        "rca_id": "3",
        "changes": {"status": "approved", "summary": "Connection pool tuning resolved saturation"}
    }
}

# 33) amend_communication (SET - update)
AMEND_COMMUNICATION = {
    "task_id": "T333",
    "function": "amend_communication",
    "params": {
        "communication_id": "3",
        "changes": {"delivery_status": "sent", "sent_at": "2025-10-02T00:30:00"}
    }
}

# 34) amend_kb_article (SET - update)
AMEND_KB_ARTICLE = {
    "task_id": "T334",
    "function": "amend_kb_article",
    "params": {
        "article_id": "3",
        "changes": {"status": "published", "reviewer_user_id": "7"}
    }
}

# 35) amend_post_incident_review (SET - update)
AMEND_POST_INCIDENT_REVIEW = {
    "task_id": "T335",
    "function": "amend_post_incident_review",
    "params": {
        "pir_id": "3",
        "changes": {"status": "in_progress", "scheduled_date": "2025-12-11"}
    }
}

# 36) set_incident_resolved (SET - resolve)
SET_INCIDENT_RESOLVED = {
    "task_id": "T336",
    "function": "set_incident_resolved",
    "params": {
        "incident_id": "3",
        "resolved_by": "5",
        "resolution_summary": "Autoscaling and pool tuning stabilized DB"
    }
}

# 37) conclude_incident (SET - close)
CONCLUDE_INCIDENT = {
    "task_id": "T337",
    "function": "conclude_incident",
    "params": {
        "incident_id": "3",
        "closed_by": "5"
    }
}

# 38) determine_severity (SET - compute/helper)
DETERMINE_SEVERITY = {
    "task_id": "T338",
    "function": "determine_severity",
    "params": {
        "complete_outage": False,
        "client_count_impacted": 5,
        "has_workaround": True,
        "regulatory_or_financial_impact": False,
        "is_priority_client": True
    }
}

# 39) record_audit_trail (SET - log)
RECORD_AUDIT_TRAIL = {
    "task_id": "T339",
    "function": "record_audit_trail",
    "params": {
        "user_id": "5",
        "action": "update",
        "reference_type": "incident",
        "reference_id": "3",
        "field_name": "status",
        "old_value": "in_progress",
        "new_value": "resolved"
    }
}

# 40) handoff_to_human (SET - control)
HANDOFF_TO_HUMAN = {
    "task_id": "T340",
    "function": "handoff_to_human",
    "params": {
        "reason_code": "policy_exception",
        "details": "Approval missing from executive for emergency rollback"
    }
}

# 41) retrieve_incident (GET)
RETRIEVE_INCIDENT = {
    "task_id": "T341",
    "function": "retrieve_incident",
    "params": {
        "incident_id": "3"
    }
}

# 42) retrieve_event_records (GET)
RETRIEVE_EVENT_RECORDS = {
    "task_id": "T342",
    "function": "retrieve_event_records",
    "params": {
        "source": "alert_log",
        "severity_hint": "P2"
    }
}

# 43) retrieve_escalations (GET)
RETRIEVE_ESCALATIONS = {
    "task_id": "T343",
    "function": "retrieve_escalations",
    "params": {
        "incident_id": "3",
        "status": "acknowledged"
    }
}

# 44) retrieve_communications (GET)
RETRIEVE_COMMUNICATIONS = {
    "task_id": "T344",
    "function": "retrieve_communications",
    "params": {
        "incident_id": "3",
        "delivery_status": "sent"
    }
}

# 45) retrieve_kb_articles (GET)
RETRIEVE_KB_ARTICLES = {
    "task_id": "T345",
    "function": "retrieve_kb_articles",
    "params": {
        "category": "incident_resolution",
        "status": "published"
    }
}

# 46) validate_approval (GET)
VALIDATE_APPROVAL = {
    "task_id": "T346",
    "function": "validate_approval",
    "params": {
        "reference_type": "change_request",
        "reference_id": "3",
        "requested_action": "schedule",
        "approver_id": "7"
    }
}

# All tasks for Interface 3 (synonym API names)
INTERFACE_3_TASKS = [
    LOCATE_ENTITIES,
    APPEND_EVENT_RECORD,
    LINK_EVENTS_ONCE,
    ENROLL_CLIENT,
    ENLIST_USER,
    ENROLL_VENDOR,
    CATALOG_PRODUCT,
    CATALOG_COMPONENT,
    INITIATE_SUBSCRIPTION,
    ESTABLISH_SLA,
    FILE_INCIDENT,
    CAPTURE_COMMUNICATION,
    DEPLOY_WORKAROUND,
    LAUNCH_RCA,
    INITIATE_ESCALATION,
    RAISE_CHANGE_REQUEST,
    REQUEST_ROLLBACK,
    CAPTURE_METRIC,
    COMPOSE_INCIDENT_REPORT,
    AUTHOR_KB_ARTICLE,
    ARRANGE_POST_INCIDENT_REVIEW,
    AMEND_CLIENT,
    AMEND_USER_PERMISSIONS,
    AMEND_PRODUCT,
    AMEND_COMPONENT,
    AMEND_SUBSCRIPTION,
    AMEND_SLA,
    AMEND_INCIDENT,
    AMEND_ESCALATION,
    AMEND_CHANGE_REQUEST,
    AMEND_ROLLBACK_REQUEST,
    AMEND_RCA,
    AMEND_COMMUNICATION,
    AMEND_KB_ARTICLE,
    AMEND_POST_INCIDENT_REVIEW,
    SET_INCIDENT_RESOLVED,
    CONCLUDE_INCIDENT,
    DETERMINE_SEVERITY,
    RECORD_AUDIT_TRAIL,
    HANDOFF_TO_HUMAN,
    RETRIEVE_INCIDENT,
    RETRIEVE_EVENT_RECORDS,
    RETRIEVE_ESCALATIONS,
    RETRIEVE_COMMUNICATIONS,
    RETRIEVE_KB_ARTICLES,
    VALIDATE_APPROVAL,
]


def get_task_by_id(task_id):
    """Get a specific task by its ID (Interface 3)"""
    for task in INTERFACE_3_TASKS:
        if task["task_id"] == task_id:
            return task
    return None


def get_tasks_by_function(function_name):
    """Get all tasks for a specific function (Interface 3)"""
    return [task for task in INTERFACE_3_TASKS if task["function"] == function_name]


def get_all_tasks():
    """Get all tasks for Interface 3"""
    return INTERFACE_3_TASKS


def get_task_count():
    """Get the total number of Interface 3 tasks"""
    return len(INTERFACE_3_TASKS)
