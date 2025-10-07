"""
Interface 4 Tasks - Incident Management Domain.

This module contains example tasks for testing the functionality of Interface 4
in the incident management domain. These tasks demonstrate the basic operations
for creating, retrieving, and managing incidents, problems, vendor engagements,
changes, communications, monitoring events, simulations, tool usage, and audits.
"""

# NOTE:
# - IDs are strings.
# - Timestamps are ISO-8601 strings when present.
# - Enum values follow the Incident Management Policy & SOPs.


# -------------------------
# Example Tasks (46 total)
# -------------------------

# 1) identify_entities (GET)
IDENTIFY_ENTITIES = {
    "task_id": "T401",
    "function": "identify_entities",
    "params": {
        "entity_type": "incident",
        "filters": {"client_id": "1", "status": "open"},
        "requester_id": "1"
    }
}

# 2) record_event_entry (SET)
RECORD_EVENT_ENTRY = {
    "task_id": "T402",
    "function": "record_event_entry",
    "params": {
        "source": "alert_log",
        "payload_summary": "High CPU on web gateway",
        "severity_hint": "P3",
        "recorded_by_id": "1"
    }
}

# 3) associate_events_once (SET)
ASSOCIATE_EVENTS_ONCE = {
    "task_id": "T403",
    "function": "associate_events_once",
    "params": {
        "event_ids": ["10", "11"],
        "correlation_key": "SIG-GW-CPU-2025",
        "link_incident_id": "4"
    }
}

# 4) register_customer (SET)
REGISTER_CUSTOMER = {
    "task_id": "T404",
    "function": "register_customer",
    "params": {
        "name": "Hooli PLC",
        "registration_number": "998877665",
        "contact_email": "ops@hooli.example",
        "client_type": "enterprise",
        "contact_phone": "+14155551000",
        "address": "1 Innovation Dr, SF CA"
    }
}

# 5) register_user (SET)
REGISTER_USER = {
    "task_id": "T405",
    "function": "register_user",
    "params": {
        "name": "Sam Carter",
        "email": "sam.carter@hooli.example",
        "role": "incident_manager",
        "timezone": "America/Los_Angeles",
        "client_id": "4"
    }
}

# 6) onboard_supplier (SET)
ONBOARD_SUPPLIER = {
    "task_id": "T406",
    "function": "onboard_supplier",
    "params": {
        "vendor_name": "EdgeShield Security",
        "contact_email": "support@edgeshield.example",
        "contact_phone": "+13125551234",
        "vendor_type": "software_provider"
    }
}

# 7) add_product_record (SET)
ADD_PRODUCT_RECORD = {
    "task_id": "T407",
    "function": "add_product_record",
    "params": {
        "product_name": "EdgeShield WAF",
        "product_type": "security_service",
        "version": "2.9.0",
        "vendor_id": "5"
    }
}

# 8) add_component_record (SET)
ADD_COMPONENT_RECORD = {
    "task_id": "T408",
    "function": "add_component_record",
    "params": {
        "product_id": "5",
        "component_name": "waf-gw-prod",
        "component_type": "firewall",
        "environment": "production",
        "location": "us-west-2",
        "ports": "443",
        "status": "online"
    }
}

# 9) provision_subscription (SET)
PROVISION_SUBSCRIPTION = {
    "task_id": "T409",
    "function": "provision_subscription",
    "params": {
        "client_id": "4",
        "product_id": "5",
        "subscription_type": "full_service",
        "service_level_tier": "premium",
        "start_date": "2025-04-01",
        "end_date": None,
        "recovery_objectives": "RTO 4h / RPO 30m"
    }
}

# 10) specify_sla (SET)
SPECIFY_SLA = {
    "task_id": "T410",
    "function": "specify_sla",
    "params": {
        "subscription_id": "5",
        "severity_level": "P2",
        "response_time_minutes": 45,
        "resolution_time_hours": 12,
        "availability_target": 99.9
    }
}

# 11) log_incident (SET)
LOG_INCIDENT = {
    "task_id": "T411",
    "function": "log_incident",
    "params": {
        "reporter_id": "9",
        "client_id": "4",
        "title": "WAF latency impacting checkout",
        "description": "Spike in TLS handshake time causing slow requests",
        "category": "performance_degradation",
        "severity": "P2",
        "impact_level": "high",
        "component_id": "6"
    }
}

# 12) record_communication_entry (SET)
RECORD_COMMUNICATION_ENTRY = {
    "task_id": "T412",
    "function": "record_communication_entry",
    "params": {
        "incident_id": "6",
        "sender_user": "9",
        "recipient": "executive_team",
        "delivery_method": "incident_portal_update",
        "message_content": "Mitigation is being applied; next update in 15 minutes."
    }
}

# 13) enact_workaround (SET)
ENACT_WORKAROUND = {
    "task_id": "T413",
    "function": "enact_workaround",
    "params": {
        "incident_id": "6",
        "description": "Temporarily disable aggressive ruleset",
        "effectiveness": "effective",
        "implemented_by": "9"
    }
}

# 14) initiate_root_cause (SET)
INITIATE_ROOT_CAUSE = {
    "task_id": "T414",
    "function": "initiate_root_cause",
    "params": {
        "incident_id": "6",
        "analysis_method": "fault_tree_analysis",
        "assigned_to": "10"
    }
}

# 15) escalate_incident (SET)
ESCALATE_INCIDENT = {
    "task_id": "T415",
    "function": "escalate_incident",
    "params": {
        "incident_id": "6",
        "target_user": "11",
        "reason": "client_demand",
        "requested_by": "9",
        "escalation_level": "executive"
    }
}

# 16) file_change_request (SET)
FILE_CHANGE_REQUEST = {
    "task_id": "T416",
    "function": "file_change_request",
    "params": {
        "change_title": "Tune WAF TLS settings and caching",
        "change_type": "normal",
        "risk_level": "medium",
        "requested_by": "9",
        "incident_id": "6"
    }
}

# 17) file_rollback_request (SET)
FILE_ROLLBACK_REQUEST = {
    "task_id": "T417",
    "function": "file_rollback_request",
    "params": {
        "change_id": "6",
        "justification": "New config increased false positives",
        "requested_by": "9",
        "incident_id": "6"
    }
}

# 18) record_metric_entry (SET)
RECORD_METRIC_ENTRY = {
    "task_id": "T418",
    "function": "record_metric_entry",
    "params": {
        "incident_id": "6",
        "metric_type": "mean_time_to_resolve",
        "calculated_value_minutes": 180,
        "target_minutes": 240
    }
}

# 19) generate_incident_summary (SET)
GENERATE_INCIDENT_SUMMARY = {
    "task_id": "T419",
    "function": "generate_incident_summary",
    "params": {
        "incident_id": "6",
        "report_type": "executive_summary",
        "generated_by": "9"
    }
}

# 20) publish_kb_article (SET)
PUBLISH_KB_ARTICLE = {
    "task_id": "T420",
    "function": "publish_kb_article",
    "params": {
        "title": "WAF Latency Troubleshooting",
        "content_type": "troubleshooting",
        "category": "incident_resolution",
        "author_id": "9",
        "incident_id": "6",
        "reviewer_user_id": "11"
    }
}

# 21) schedule_pir_session (SET)
SCHEDULE_PIR_SESSION = {
    "task_id": "T421",
    "function": "schedule_pir_session",
    "params": {
        "incident_id": "6",
        "scheduled_date": "2025-12-15",
        "facilitator_user_id": "9"
    }
}

# 22) alter_client (SET - update)
ALTER_CLIENT = {
    "task_id": "T422",
    "function": "alter_client",
    "params": {
        "client_id": "4",
        "changes": {"status": "active", "address": "2 Innovation Dr, SF CA"},
        "requester_id": "9"
    }
}

# 23) alter_user_permissions (SET - update)
ALTER_USER_PERMISSIONS = {
    "task_id": "T423",
    "function": "alter_user_permissions",
    "params": {
        "user_id": "11",
        "requested_changes": {"role": "executive", "status": "active"},
        "modified_by": "9"
    }
}

# 24) alter_product (SET - update)
ALTER_PRODUCT = {
    "task_id": "T424",
    "function": "alter_product",
    "params": {
        "product_id": "5",
        "changes": {"version": "2.9.1", "status": "active"}
    }
}

# 25) alter_component (SET - update)
ALTER_COMPONENT = {
    "task_id": "T425",
    "function": "alter_component",
    "params": {
        "component_id": "6",
        "changes": {"status": "maintenance", "environment": "staging"}
    }
}

# 26) alter_subscription (SET - update)
ALTER_SUBSCRIPTION = {
    "task_id": "T426",
    "function": "alter_subscription",
    "params": {
        "subscription_id": "5",
        "changes": {"service_level_tier": "standard", "rto_hours": 8}
    }
}

# 27) alter_sla (SET - update)
ALTER_SLA = {
    "task_id": "T427",
    "function": "alter_sla",
    "params": {
        "sla_id": "5",
        "changes": {"response_time_minutes": 30, "status": "active"}
    }
}

# 28) alter_incident (SET - update)
ALTER_INCIDENT = {
    "task_id": "T428",
    "function": "alter_incident",
    "params": {
        "incident_id": "6",
        "new_status": "in_progress",
        "field_updates": {"assigned_manager_id": "9", "severity": "P2"},
        "updated_by": "9"
    }
}

# 29) alter_escalation (SET - update)
ALTER_ESCALATION = {
    "task_id": "T429",
    "function": "alter_escalation",
    "params": {
        "escalation_id": "6",
        "changes": {"status": "acknowledged", "acknowledged_at": "2025-10-02T01:25:00"}
    }
}

# 30) alter_change_request (SET - update)
ALTER_CHANGE_REQUEST = {
    "task_id": "T430",
    "function": "alter_change_request",
    "params": {
        "change_id": "6",
        "changes": {"status": "scheduled", "scheduled_start": "2025-10-06T03:00:00"}
    }
}

# 31) alter_rollback_request (SET - update)
ALTER_ROLLBACK_REQUEST = {
    "task_id": "T431",
    "function": "alter_rollback_request",
    "params": {
        "rollback_id": "6",
        "changes": {"status": "approved", "approved_by_id": "11"}
    }
}

# 32) alter_rca (SET - update)
ALTER_RCA = {
    "task_id": "T432",
    "function": "alter_rca",
    "params": {
        "rca_id": "6",
        "changes": {"status": "completed", "summary": "TLS config regression identified"}
    }
}

# 33) alter_communication (SET - update)
ALTER_COMMUNICATION = {
    "task_id": "T433",
    "function": "alter_communication",
    "params": {
        "communication_id": "6",
        "changes": {"delivery_status": "delivered", "sent_at": "2025-10-02T00:45:00"}
    }
}

# 34) alter_kb_article (SET - update)
ALTER_KB_ARTICLE = {
    "task_id": "T434",
    "function": "alter_kb_article",
    "params": {
        "article_id": "6",
        "changes": {"status": "published", "reviewer_user_id": "11"}
    }
}

# 35) alter_post_incident_review (SET - update)
ALTER_POST_INCIDENT_REVIEW = {
    "task_id": "T435",
    "function": "alter_post_incident_review",
    "params": {
        "pir_id": "6",
        "changes": {"status": "in_progress", "scheduled_date": "2025-12-16"}
    }
}

# 36) flag_incident_resolved (SET - resolve)
FLAG_INCIDENT_RESOLVED = {
    "task_id": "T436",
    "function": "flag_incident_resolved",
    "params": {
        "incident_id": "6",
        "resolved_by": "9",
        "resolution_summary": "Ruleset tuned; latency normalized"
    }
}

# 37) finalize_case (SET - close)
FINALIZE_CASE = {
    "task_id": "T437",
    "function": "finalize_case",
    "params": {
        "incident_id": "6",
        "closed_by": "9"
    }
}

# 38) rate_severity (SET - compute/helper)
RATE_SEVERITY = {
    "task_id": "T438",
    "function": "rate_severity",
    "params": {
        "complete_outage": False,
        "client_count_impacted": 2,
        "has_workaround": True,
        "regulatory_or_financial_impact": False,
        "is_priority_client": False
    }
}

# 39) write_audit_entry (SET - log)
WRITE_AUDIT_ENTRY = {
    "task_id": "T439",
    "function": "write_audit_entry",
    "params": {
        "user_id": "9",
        "action": "update",
        "reference_type": "incident",
        "reference_id": "6",
        "field_name": "status",
        "old_value": "in_progress",
        "new_value": "resolved"
    }
}

# 40) route_to_human (SET - control)
ROUTE_TO_HUMAN = {
    "task_id": "T440",
    "function": "route_to_human",
    "params": {
        "reason_code": "approval_blocker",
        "details": "Executive approval missing for emergency change"
    }
}

# 41) pull_incident (GET)
PULL_INCIDENT = {
    "task_id": "T441",
    "function": "pull_incident",
    "params": {
        "incident_id": "6"
    }
}

# 42) pull_event_records (GET)
PULL_EVENT_RECORDS = {
    "task_id": "T442",
    "function": "pull_event_records",
    "params": {
        "source": "alert_log",
        "severity_hint": "P3"
    }
}

# 43) pull_escalations (GET)
PULL_ESCALATIONS = {
    "task_id": "T443",
    "function": "pull_escalations",
    "params": {
        "incident_id": "6",
        "status": "acknowledged"
    }
}

# 44) pull_communications (GET)
PULL_COMMUNICATIONS = {
    "task_id": "T444",
    "function": "pull_communications",
    "params": {
        "incident_id": "6",
        "delivery_status": "delivered"
    }
}

# 45) pull_kb_articles (GET)
PULL_KB_ARTICLES = {
    "task_id": "T445",
    "function": "pull_kb_articles",
    "params": {
        "category": "incident_resolution",
        "status": "published"
    }
}

# 46) confirm_approval_status (GET)
CONFIRM_APPROVAL_STATUS = {
    "task_id": "T446",
    "function": "confirm_approval_status",
    "params": {
        "reference_type": "change_request",
        "reference_id": "6",
        "requested_action": "schedule",
        "approver_id": "11"
    }
}


INTERFACE_4_TASKS = [
    IDENTIFY_ENTITIES,
    RECORD_EVENT_ENTRY,
    ASSOCIATE_EVENTS_ONCE,
    REGISTER_CUSTOMER,
    REGISTER_USER,
    ONBOARD_SUPPLIER,
    ADD_PRODUCT_RECORD,
    ADD_COMPONENT_RECORD,
    PROVISION_SUBSCRIPTION,
    SPECIFY_SLA,
    LOG_INCIDENT,
    RECORD_COMMUNICATION_ENTRY,
    ENACT_WORKAROUND,
    INITIATE_ROOT_CAUSE,
    ESCALATE_INCIDENT,
    FILE_CHANGE_REQUEST,
    FILE_ROLLBACK_REQUEST,
    RECORD_METRIC_ENTRY,
    GENERATE_INCIDENT_SUMMARY,
    PUBLISH_KB_ARTICLE,
    SCHEDULE_PIR_SESSION,
    ALTER_CLIENT,
    ALTER_USER_PERMISSIONS,
    ALTER_PRODUCT,
    ALTER_COMPONENT,
    ALTER_SUBSCRIPTION,
    ALTER_SLA,
    ALTER_INCIDENT,
    ALTER_ESCALATION,
    ALTER_CHANGE_REQUEST,
    ALTER_ROLLBACK_REQUEST,
    ALTER_RCA,
    ALTER_COMMUNICATION,
    ALTER_KB_ARTICLE,
    ALTER_POST_INCIDENT_REVIEW,
    FLAG_INCIDENT_RESOLVED,
    FINALIZE_CASE,
    RATE_SEVERITY,
    WRITE_AUDIT_ENTRY,
    ROUTE_TO_HUMAN,
    PULL_INCIDENT,
    PULL_EVENT_RECORDS,
    PULL_ESCALATIONS,
    PULL_COMMUNICATIONS,
    PULL_KB_ARTICLES,
    CONFIRM_APPROVAL_STATUS,
]


def get_task_by_id(task_id):
    """Get a specific task by its ID (Interface 4)"""
    for task in INTERFACE_4_TASKS:
        if task["task_id"] == task_id:
            return task
    return None


def get_tasks_by_function(function_name):
    """Get all tasks for a specific function (Interface 4)"""
    return [task for task in INTERFACE_4_TASKS if task["function"] == function_name]


def get_all_tasks():
    """Get all tasks for Interface 4"""
    return INTERFACE_4_TASKS


def get_task_count():
    """Get the total number of Interface 4 tasks"""
    return len(INTERFACE_4_TASKS)
