"""
Interface 5 Tasks - Incident Management Domain.

This module contains example tasks for testing the functionality of Interface 5
in the incident management domain. These tasks demonstrate the basic operations
for creating, retrieving, and managing incidents, problems, vendor engagements,
changes, communications, monitoring events, simulations, tool usage, and audits.
"""

# NOTE:
# - IDs are strings.
# - Timestamps are ISO-8601 strings when present.
# - Enum values follow the Incident Management Policy & SOPs.

# 1) survey_entities (GET)
SURVEY_ENTITIES = {
    "task_id": "T501",
    "function": "survey_entities",
    "params": {
        "entity_type": "incident",
        "filters": {"client_id": "1", "status": "open"},
        "requester_id": "1"
    }
}

# 2) ingest_event_record (SET)
INGEST_EVENT_RECORD = {
    "task_id": "T502",
    "function": "ingest_event_record",
    "params": {
        "source": "alert_log",
        "payload_summary": "Disk space warning on DB node",
        "severity_hint": "P3",
        "recorded_by_id": "1"
    }
}

# 3) match_events_once (SET)
MATCH_EVENTS_ONCE = {
    "task_id": "T503",
    "function": "match_events_once",
    "params": {
        "event_ids": ["20", "21"],
        "correlation_key": "SIG-DB-DISK-2025",
        "link_incident_id": "8"
    }
}

# 4) onboard_client (SET)
ONBOARD_CLIENT = {
    "task_id": "T504",
    "function": "onboard_client",
    "params": {
        "name": "Aperture Labs GmbH",
        "registration_number": "123450987",
        "contact_email": "it@aperture.example",
        "client_type": "mid_market",
        "contact_phone": "+49891234567",
        "address": "Science Park 1, Munich"
    }
}

# 5) enroll_user (SET)
ENROLL_USER = {
    "task_id": "T505",
    "function": "enroll_user",
    "params": {
        "name": "Chell Johnson",
        "email": "chell.j@aperture.example",
        "role": "technical_support",
        "timezone": "Europe/Berlin",
        "client_id": "7"
    }
}

# 6) enlist_vendor (SET)
ENLIST_VENDOR = {
    "task_id": "T506",
    "function": "enlist_vendor",
    "params": {
        "vendor_name": "PortalOps Cloud",
        "contact_email": "support@portalops.example",
        "contact_phone": "+442071234567",
        "vendor_type": "cloud_service_provider"
    }
}

# 7) catalogue_product (SET)
CATALOGUE_PRODUCT = {
    "task_id": "T507",
    "function": "catalogue_product",
    "params": {
        "product_name": "PortalOps DBaaS",
        "product_type": "other",
        "version": "5.4.1",
        "vendor_id": "9"
    }
}

# 8) catalogue_component (SET)
CATALOGUE_COMPONENT = {
    "task_id": "T508",
    "function": "catalogue_component",
    "params": {
        "product_id": "9",
        "component_name": "db-primary-eu",
        "component_type": "database",
        "environment": "production",
        "location": "eu-central-1",
        "ports": "5432",
        "status": "online"
    }
}

# 9) activate_subscription (SET)
ACTIVATE_SUBSCRIPTION = {
    "task_id": "T509",
    "function": "activate_subscription",
    "params": {
        "client_id": "7",
        "product_id": "9",
        "subscription_type": "full_service",
        "service_level_tier": "standard",
        "start_date": "2025-04-10",
        "end_date": None,
        "recovery_objectives": "RTO 8h / RPO 1h"
    }
}

# 10) set_sla (SET)
SET_SLA = {
    "task_id": "T510",
    "function": "set_sla",
    "params": {
        "subscription_id": "9",
        "severity_level": "P3",
        "response_time_minutes": 120,
        "resolution_time_hours": 24,
        "availability_target": 99.5
    }
}

# 11) report_incident (SET)
REPORT_INCIDENT = {
    "task_id": "T511",
    "function": "report_incident",
    "params": {
        "reporter_id": "12",
        "client_id": "7",
        "title": "DB connection pool exhaustion",
        "description": "Frequent timeouts during peak hours",
        "category": "performance_degradation",
        "severity": "P2",
        "impact_level": "high",
        "component_id": "10"
    }
}

# 12) log_interaction (SET)
LOG_INTERACTION = {
    "task_id": "T512",
    "function": "log_interaction",
    "params": {
        "incident_id": "10",
        "sender_user": "12",
        "recipient": "client_contact",
        "delivery_method": "chat",
        "message_content": "We are scaling read replicas to mitigate load."
    }
}

# 13) apply_mitigation (SET)
APPLY_MITIGATION = {
    "task_id": "T513",
    "function": "apply_mitigation",
    "params": {
        "incident_id": "10",
        "description": "Increase max_connections and add one replica",
        "effectiveness": "partially_effective",
        "implemented_by": "12"
    }
}

# 14) commence_rca (SET)
COMMENCE_RCA = {
    "task_id": "T514",
    "function": "commence_rca",
    "params": {
        "incident_id": "10",
        "analysis_method": "five_whys",
        "assigned_to": "13"
    }
}

# 15) trigger_escalation (SET)
TRIGGER_ESCALATION = {
    "task_id": "T515",
    "function": "trigger_escalation",
    "params": {
        "incident_id": "10",
        "target_user": "14",
        "reason": "severity_increase",
        "requested_by": "12",
        "escalation_level": "management"
    }
}

# 16) propose_change_request (SET)
PROPOSE_CHANGE_REQUEST = {
    "task_id": "T516",
    "function": "propose_change_request",
    "params": {
        "change_title": "Reconfigure connection pooling and autoscaling",
        "change_type": "standard",
        "risk_level": "low",
        "requested_by": "12",
        "incident_id": "10"
    }
}

# 17) raise_rollback_request (SET)
RAISE_ROLLBACK_REQUEST = {
    "task_id": "T517",
    "function": "raise_rollback_request",
    "params": {
        "change_id": "10",
        "justification": "Unexpected latency after parameter change",
        "requested_by": "12",
        "incident_id": "10"
    }
}

# 18) track_metric (SET)
TRACK_METRIC = {
    "task_id": "T518",
    "function": "track_metric",
    "params": {
        "incident_id": "10",
        "metric_type": "mean_time_to_detect",
        "calculated_value_minutes": 35,
        "target_minutes": 30
    }
}

# 19) compile_incident_report (SET)
COMPILE_INCIDENT_REPORT = {
    "task_id": "T519",
    "function": "compile_incident_report",
    "params": {
        "incident_id": "10",
        "report_type": "postmortem_report",
        "generated_by": "12"
    }
}

# 20) author_kb_draft (SET)
AUTHOR_KB_DRAFT = {
    "task_id": "T520",
    "function": "author_kb_draft",
    "params": {
        "title": "DB Pool Exhaustion Playbook",
        "content_type": "prevention_guide",
        "category": "best_practice",
        "author_id": "12",
        "incident_id": "10",
        "reviewer_user_id": "14"
    }
}

# 21) plan_post_incident_review (SET)
PLAN_POST_INCIDENT_REVIEW = {
    "task_id": "T521",
    "function": "plan_post_incident_review",
    "params": {
        "incident_id": "10",
        "scheduled_date": "2026-01-20",
        "facilitator_user_id": "12"
    }
}

# 22) revise_client (SET - update)
REVISE_CLIENT = {
    "task_id": "T522",
    "function": "revise_client",
    "params": {
        "client_id": "7",
        "changes": {"status": "active", "contact_phone": "+49891234000"},
        "requester_id": "12"
    }
}

# 23) adjust_user_permissions (SET - update)
ADJUST_USER_PERMISSIONS = {
    "task_id": "T523",
    "function": "adjust_user_permissions",
    "params": {
        "user_id": "14",
        "requested_changes": {"role": "incident_manager", "status": "active"},
        "modified_by": "12"
    }
}

# 24) revise_product (SET - update)
REVISE_PRODUCT = {
    "task_id": "T524",
    "function": "revise_product",
    "params": {
        "product_id": "9",
        "changes": {"version": "5.5.0", "status": "active"}
    }
}

# 25) revise_component (SET - update)
REVISE_COMPONENT = {
    "task_id": "T525",
    "function": "revise_component",
    "params": {
        "component_id": "10",
        "changes": {"status": "degraded", "environment": "staging"}
    }
}

# 26) revise_subscription (SET - update)
REVISE_SUBSCRIPTION = {
    "task_id": "T526",
    "function": "revise_subscription",
    "params": {
        "subscription_id": "9",
        "changes": {"service_level_tier": "premium", "rto_hours": 4}
    }
}

# 27) revise_sla (SET - update)
REVISE_SLA = {
    "task_id": "T527",
    "function": "revise_sla",
    "params": {
        "sla_id": "9",
        "changes": {"response_time_minutes": 90, "status": "active"}
    }
}

# 28) revise_incident (SET - update)
REVISE_INCIDENT = {
    "task_id": "T528",
    "function": "revise_incident",
    "params": {
        "incident_id": "10",
        "new_status": "in_progress",
        "field_updates": {"assigned_manager_id": "12", "urgency": "high"},
        "updated_by": "12"
    }
}

# 29) revise_escalation (SET - update)
REVISE_ESCALATION = {
    "task_id": "T529",
    "function": "revise_escalation",
    "params": {
        "escalation_id": "10",
        "changes": {"status": "resolved", "resolved_at": "2025-10-03T10:10:00"}
    }
}

# 30) revise_change_request (SET - update)
REVISE_CHANGE_REQUEST = {
    "task_id": "T530",
    "function": "revise_change_request",
    "params": {
        "change_id": "10",
        "changes": {"status": "in_progress", "actual_start": "2025-10-04T02:00:00"}
    }
}

# 31) revise_rollback_request (SET - update)
REVISE_ROLLBACK_REQUEST = {
    "task_id": "T531",
    "function": "revise_rollback_request",
    "params": {
        "rollback_id": "10",
        "changes": {"status": "completed", "executed_at": "2025-10-04T04:30:00"}
    }
}

# 32) revise_rca (SET - update)
REVISE_RCA = {
    "task_id": "T532",
    "function": "revise_rca",
    "params": {
        "rca_id": "10",
        "changes": {"status": "approved", "summary": "Peak traffic pattern not forecasted"}
    }
}

# 33) revise_communication (SET - update)
REVISE_COMMUNICATION = {
    "task_id": "T533",
    "function": "revise_communication",
    "params": {
        "communication_id": "10",
        "changes": {"delivery_status": "sent", "sent_at": "2025-10-03T09:45:00"}
    }
}

# 34) revise_kb_article (SET - update)
REVISE_KB_ARTICLE = {
    "task_id": "T534",
    "function": "revise_kb_article",
    "params": {
        "article_id": "10",
        "changes": {"status": "archived"}
    }
}

# 35) revise_post_incident_review (SET - update)
REVISE_POST_INCIDENT_REVIEW = {
    "task_id": "T535",
    "function": "revise_post_incident_review",
    "params": {
        "pir_id": "10",
        "changes": {"status": "completed", "timeline_accuracy_rating": 4}
    }
}

# 36) settle_incident (SET - resolve)
SETTLE_INCIDENT = {
    "task_id": "T536",
    "function": "settle_incident",
    "params": {
        "incident_id": "10",
        "resolved_by": "12",
        "resolution_summary": "Autoscaling and pool tuning resolved timeouts"
    }
}

# 37) wrap_up_incident (SET - close)
WRAP_UP_INCIDENT = {
    "task_id": "T537",
    "function": "wrap_up_incident",
    "params": {
        "incident_id": "10",
        "closed_by": "12"
    }
}

# 38) evaluate_severity (SET - compute/helper)
EVALUATE_SEVERITY = {
    "task_id": "T538",
    "function": "evaluate_severity",
    "params": {
        "complete_outage": False,
        "client_count_impacted": 3,
        "has_workaround": True,
        "regulatory_or_financial_impact": False,
        "is_priority_client": True
    }
}

# 39) log_audit_entry (SET - log)
LOG_AUDIT_ENTRY = {
    "task_id": "T539",
    "function": "log_audit_entry",
    "params": {
        "user_id": "12",
        "action": "update",
        "reference_type": "incident",
        "reference_id": "10",
        "field_name": "status",
        "old_value": "in_progress",
        "new_value": "resolved"
    }
}

# 40) hand_off_to_human (SET - control)
HAND_OFF_TO_HUMAN = {
    "task_id": "T540",
    "function": "hand_off_to_human",
    "params": {
        "reason_code": "policy_conflict",
        "details": "Change requires CAB approval outside automation scope"
    }
}

# 41) read_incident (GET)
READ_INCIDENT = {
    "task_id": "T541",
    "function": "read_incident",
    "params": {
        "incident_id": "10"
    }
}

# 42) read_event_records (GET)
READ_EVENT_RECORDS = {
    "task_id": "T542",
    "function": "read_event_records",
    "params": {
        "source": "alert_log",
        "severity_hint": "P3"
    }
}

# 43) read_escalations (GET)
READ_ESCALATIONS = {
    "task_id": "T543",
    "function": "read_escalations",
    "params": {
        "incident_id": "10",
        "status": "resolved"
    }
}

# 44) read_communications (GET)
READ_COMMUNICATIONS = {
    "task_id": "T544",
    "function": "read_communications",
    "params": {
        "incident_id": "10",
        "delivery_status": "sent"
    }
}

# 45) read_kb_articles (GET)
READ_KB_ARTICLES = {
    "task_id": "T545",
    "function": "read_kb_articles",
    "params": {
        "category": "best_practice",
        "status": "published"
    }
}

# 46) confirm_approval (GET)
CONFIRM_APPROVAL = {
    "task_id": "T546",
    "function": "confirm_approval",
    "params": {
        "reference_type": "change_request",
        "reference_id": "10",
        "requested_action": "schedule",
        "approver_id": "14"
    }
}


INTERFACE_5_TASKS = [
    SURVEY_ENTITIES,
    INGEST_EVENT_RECORD,
    MATCH_EVENTS_ONCE,
    ONBOARD_CLIENT,
    ENROLL_USER,
    ENLIST_VENDOR,
    CATALOGUE_PRODUCT,
    CATALOGUE_COMPONENT,
    ACTIVATE_SUBSCRIPTION,
    SET_SLA,
    REPORT_INCIDENT,
    LOG_INTERACTION,
    APPLY_MITIGATION,
    COMMENCE_RCA,
    TRIGGER_ESCALATION,
    PROPOSE_CHANGE_REQUEST,
    RAISE_ROLLBACK_REQUEST,
    TRACK_METRIC,
    COMPILE_INCIDENT_REPORT,
    AUTHOR_KB_DRAFT,
    PLAN_POST_INCIDENT_REVIEW,
    REVISE_CLIENT,
    ADJUST_USER_PERMISSIONS,
    REVISE_PRODUCT,
    REVISE_COMPONENT,
    REVISE_SUBSCRIPTION,
    REVISE_SLA,
    REVISE_INCIDENT,
    REVISE_ESCALATION,
    REVISE_CHANGE_REQUEST,
    REVISE_ROLLBACK_REQUEST,
    REVISE_RCA,
    REVISE_COMMUNICATION,
    REVISE_KB_ARTICLE,
    REVISE_POST_INCIDENT_REVIEW,
    SETTLE_INCIDENT,
    WRAP_UP_INCIDENT,
    EVALUATE_SEVERITY,
    LOG_AUDIT_ENTRY,
    HAND_OFF_TO_HUMAN,
    READ_INCIDENT,
    READ_EVENT_RECORDS,
    READ_ESCALATIONS,
    READ_COMMUNICATIONS,
    READ_KB_ARTICLES,
    CONFIRM_APPROVAL,
]


def get_task_by_id(task_id):
    """Get a specific task by its ID (Interface 5)"""
    for task in INTERFACE_5_TASKS:
        if task["task_id"] == task_id:
            return task
    return None


def get_tasks_by_function(function_name):
    """Get all tasks for a specific function (Interface 5)"""
    return [task for task in INTERFACE_5_TASKS if task["function"] == function_name]


def get_all_tasks():
    """Get all tasks for Interface 5"""
    return INTERFACE_5_TASKS


def get_task_count():
    """Get the total number of tasks"""
    return len(INTERFACE_5_TASKS)
