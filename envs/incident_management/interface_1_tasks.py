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


# 1) entities_lookup — read
ENTITIES_LOOKUP_TASK = {
    "task_id": "if1_task_001",
    "description": "Lookup a user by email for verification",
    "function": "entities_lookup",
    "parameters": {
        "entity_type": "user",
        "filters": {"email": "sda.jane.doe@example.com"},
        "requester_id": "101"
    },
    "expected_result": "Zero, one, or many users matching the email"
}

# 2) create_incident — create
CREATE_INCIDENT_TASK = {
    "task_id": "if1_task_002",
    "description": "Create a new incident reported by a user",
    "function": "create_incident",
    "parameters": {
        "reporter_id": "101",
        "detection_source": "user_report",
        "initial_description": "Email service is intermittently failing for multiple users."
    },
    "expected_result": "{\"incident_id\": <str>, \"status\": \"open\", \"success\": true}"
}

# 3) log_incident_details — update
LOG_INCIDENT_DETAILS_TASK = {
    "task_id": "if1_task_003",
    "description": "Append core details to an existing incident",
    "function": "log_incident_details",
    "parameters": {
        "incident_id": "2001",
        "incident_description": "Impact: company-wide email latency; suspected load spike.",
        "affected_service": "3001",
        "timestamp": "2025-10-01T00:00:00",
        "initial_diagnosis": "Possible mail queue backlog on MX-2.",
        "workaround_note": "Users advised to retry after 5 minutes."
    },
    "expected_result": "Updated incident summary reflecting new details"
}

# 4) categorize_incident — update
CATEGORIZE_INCIDENT_TASK = {
    "task_id": "if1_task_004",
    "description": "Categorize an incident as a software issue",
    "function": "categorize_incident",
    "parameters": {
        "incident_id": "2002",
        "category": "software",
        "sub_category": "email_delivery"
    },
    "expected_result": "{\"incident_id\": \"2002\", \"category\": \"software\", \"success\": true}"
}

# 5) prioritize_incident — update
PRIORITIZE_INCIDENT_TASK = {
    "task_id": "if1_task_005",
    "description": "Set incident priority to high with justification",
    "function": "prioritize_incident",
    "parameters": {
        "incident_id": "2003",
        "priority": "high",
        "justification": "Affects most end users; business-critical service impact."
    },
    "expected_result": "{\"incident_id\": \"2003\", \"priority\": \"high\", \"success\": true}"
}

# 6) assign_incident — update + create (communication)
ASSIGN_INCIDENT_TASK = {
    "task_id": "if1_task_006",
    "description": "Assign the incident to L2 and acknowledge",
    "function": "assign_incident",
    "parameters": {
        "incident_id": "2004",
        "assigned_team": "L2",
        "responder_user_id": "205",
        "communication_message": "Incident acknowledged by L2. Investigation started."
    },
    "expected_result": "{\"incident_id\": \"2004\", \"status\": \"in_progress\", \"assigned_team\": \"L2\", \"success\": true}"
}
# 7) record_diagnosis_workaround — update
RECORD_DIAGNOSIS_WORKAROUND_TASK = {
    "task_id": "if1_task_007",
    "description": "Record diagnostic steps and temporary workaround",
    "function": "record_diagnosis_workaround",
    "parameters": {
        "incident_id": "2005",
        "diagnostic_steps_summary": "Checked MX-2 queues; identified burst traffic from misconfigured agent.",
        "workaround_applied": True,
        "responder_user_id": "205",
        "workaround_details": "Throttled offending agent; reduced inbound queue size."
    },
    "expected_result": "Incident updated with diagnosis and workaround details"
}

# 8) escalate_incident — update
ESCALATE_INCIDENT_TASK = {
    "task_id": "if1_task_008",
    "description": "Escalate incident to L3 specialists",
    "function": "escalate_incident",
    "parameters": {
        "incident_id": "2006",
        "escalated_to": "L3",
        "reason_for_escalation": "Deep mail routing logic issue suspected.",
        "escalated_by_user_id": "205"
    },
    "expected_result": "{\"incident_id\": \"2006\", \"status\": \"escalated\", \"escalated_to\": \"L3\", \"success\": true}"
}

# 9) create_vendor_engagement — create/update
CREATE_VENDOR_ENGAGEMENT_TASK = {
    "task_id": "if1_task_009",
    "description": "Engage vendor via portal and mark incident pending_vendor",
    "function": "create_vendor_engagement",
    "parameters": {
        "incident_id": "2007",
        "vendor_name": "MailCloud Inc.",
        "contact_method": "vendor_portal",
        "vendor_ticket_reference": "MC-CASE-8891",
        "initiated_by_user_id": "310"
    },
    "expected_result": "{\"incident_id\": \"2007\", \"vendor_engagement_id\": <str>, \"status\": \"pending_vendor\", \"success\": true}"
}
# 10) link_change_to_incident — update
LINK_CHANGE_TO_INCIDENT_TASK = {
    "task_id": "if1_task_010",
    "description": "Record a change coordination reference for the incident",
    "function": "link_change_to_incident",
    "parameters": {
        "incident_id": "2008",
        "change_summary": "Reconfigure MX-2 routing policy and deploy hotfix.",
        "requested_by": "change_mgmt",
        "approval_record_id": "A-555"
    },
    "expected_result": "{\"incident_id\": \"2008\", \"change_link_id\": <str>, \"success\": true}"
}

# 11) resolve_incident — update
RESOLVE_INCIDENT_TASK = {
    "task_id": "if1_task_011",
    "description": "Resolve the incident after permanent fix",
    "function": "resolve_incident",
    "parameters": {
        "incident_id": "2009",
        "resolution_summary": "Applied configuration hotfix; queues normalized.",
        "resolved_by_user_id": "401",
        "resolution_timestamp": "2025-10-01T01:45:00"
    },
    "expected_result": "{\"incident_id\": \"2009\", \"status\": \"resolved\", \"success\": true}"
}

# 12) add_incident_communication — create
ADD_INCIDENT_COMMUNICATION_TASK = {
    "task_id": "if1_task_012",
    "description": "Post a stakeholder update on incident progress",
    "function": "add_incident_communication",
    "parameters": {
        "incident_id": "2010",
        "message_text": "Root cause identified; mitigation in progress. Next update in 30 minutes.",
        "recipients_group": "stakeholders",
        "sent_by_user_id": "205"
    },
    "expected_result": "{\"communication_id\": <str>, \"incident_id\": \"2010\", \"success\": true}"
}

# 13) close_incident — update
CLOSE_INCIDENT_TASK = {
    "task_id": "if1_task_013",
    "description": "Close a resolved incident with closure notes",
    "function": "close_incident",
    "parameters": {
        "incident_id": "2011",
        # service_desk_manager or incident_manager for high priority
        "closed_by_user_id": "102",
        "closure_notes": "Monitored for 2 hours; stable with normal latency."
    },
    "expected_result": "{\"incident_id\": \"2011\", \"status\": \"closed\", \"success\": true}"
}

# 14) create_post_incident_review — create
CREATE_POST_INCIDENT_REVIEW_TASK = {
    "task_id": "if1_task_014",
    "description": "Create a PIR for a high-priority incident",
    "function": "create_post_incident_review",
    "parameters": {
        "incident_id": "2012",
        "review_notes": "Timeline captured; contributing factors include misconfigured agent.",
        "conducted_by_user_id": "100"  # incident_manager
    },
    "expected_result": "{\"review_id\": <str>, \"incident_id\": \"2012\", \"success\": true}"
}

# 15) update_knowledge_base_from_incident — create/update
UPDATE_KNOWLEDGE_BASE_FROM_INCIDENT_TASK = {
    "task_id": "if1_task_015",
    "description": "Publish KB update with resolution and preventive actions",
    "function": "update_knowledge_base_from_incident",
    "parameters": {
        "incident_id": "2013",
        "kb_update_notes": "Add MX queue monitoring threshold and agent config validation checklist.",
        "submitted_by_user_id": "100"
    },
    "expected_result": "{\"kb_entry_id\": <str>, \"linked_incident_id\": \"2013\", \"success\": true}"
}

# 16) create_incident_from_monitoring_event — create
CREATE_INCIDENT_FROM_MONITORING_EVENT_TASK = {
    "task_id": "if1_task_016",
    "description": "Create an incident from an existing monitoring event",
    "function": "create_incident_from_monitoring_event",
    "parameters": {
        "monitoring_event_id": "EVT-9001",
        "detected_service": "3002",
        "alert_details": "CPU utilization sustained over 95% for 10 minutes."
    },
    "expected_result": "{\"incident_id\": <str>, \"source\": \"monitoring\", \"status\": \"open\", \"success\": true}"
}
# 17) record_tool_usage — create
RECORD_TOOL_USAGE_TASK = {
    "task_id": "if1_task_017",
    "description": "Log the use of an AIOps correlation run on an incident",
    "function": "record_tool_usage",
    "parameters": {
        "incident_id": "2014",
        "tool_used": "AIOps",
        "action_summary": "Correlated spikes to deployment window; suggested rollback.",
        "executed_by": "205"
    },
    "expected_result": "{\"tool_use_id\": <str>, \"incident_id\": \"2014\", \"success\": true}"
}

# 18) record_incident_simulation — create
RECORD_INCIDENT_SIMULATION_TASK = {
    "task_id": "if1_task_018",
    "description": "Record a simulated incident drill for the core email service",
    "function": "record_incident_simulation",
    "parameters": {
        "scenario_name": "Email outage tabletop",
        "simulated_by_user_id": "100",
        "scope": "email_service"
    },
    "expected_result": "{\"simulation_id\": <str>, \"success\": true}"
}

# 19) problem_create — create
PROBLEM_CREATE_TASK = {
    "task_id": "if1_task_019",
    "description": "Create a problem for recurring MX queue backlogs",
    "function": "problem_create",
    "parameters": {
        "problem_title": "Recurring MX queue backlog",
        "description": "Multiple incidents with queue saturation during peak hours.",
        "detection_source": "monitoring_tool",
        "created_by_user_id": "401",
        "related_incident_ids": ["2005", "2007"]
    },
    "expected_result": "{\"problem_id\": <str>, \"status\": \"open\", \"success\": true}"
}

# 20) problem_update — update
PROBLEM_UPDATE_TASK = {
    "task_id": "if1_task_020",
    "description": "Update a problem with refined scope and assignee",
    "function": "problem_update",
    "parameters": {
        "problem_id": "P-3001",
        "change_set": {
                "title": "MX backlog root cause analysis",
                "description": "Narrowed to policy engine during peak retries.",
                "assignee_user_id": "405",
                "priority": "high"
        },
        "updated_by_user_id": "401"
    },
    "expected_result": "{\"problem_id\": \"P-3001\", \"success\": true}"
}

# 21) problem_link_incident — update
PROBLEM_LINK_INCIDENT_TASK = {
    "task_id": "if1_task_021",
    "description": "Link an incident to an existing problem",
    "function": "problem_link_incident",
    "parameters": {
        "problem_id": "P-3001",
        "incident_id": "2015",
        "linked_by_user_id": "405"
    },
    "expected_result": "{\"problem_id\": \"P-3001\", \"incident_id\": \"2015\", \"success\": true}"
}

# 22) problem_add_workaround — update
PROBLEM_ADD_WORKAROUND_TASK = {
    "task_id": "if1_task_022",
    "description": "Add a workaround to the problem and publish to KB",
    "function": "problem_add_workaround",
    "parameters": {
        "problem_id": "P-3002",
        "workaround_summary": "Temporarily reduce retry rate; auto-drain queues nightly.",
        "added_by_user_id": "405"
    },
    "expected_result": "{\"problem_id\": \"P-3002\", \"status\": \"workaround_available\", \"kb_link_id\": <str>, \"success\": true}"
}

# 23) problem_resolve — update
PROBLEM_RESOLVE_TASK = {
    "task_id": "if1_task_023",
    "description": "Resolve the problem with a validated permanent fix",
    "function": "problem_resolve",
    "parameters": {
        "problem_id": "P-3003",
        "permanent_fix_summary": "Policy engine patch v2.1; adaptive retry backoff.",
        "validation_evidence": "Post-patch monitoring shows stable queues over 7 days.",
        "resolved_by_user_id": "405"
    },
    "expected_result": "{\"problem_id\": \"P-3003\", \"status\": \"resolved\", \"success\": true}"
}

# 24) problem_close — update
PROBLEM_CLOSE_TASK = {
    "task_id": "if1_task_024",
    "description": "Close a resolved problem after stability window",
    "function": "problem_close",
    "parameters": {
        "problem_id": "P-3003",
        "closed_by_user_id": "100",
        "closure_notes": "Stable over 14 days; no reoccurrences."
    },
    "expected_result": "{\"problem_id\": \"P-3003\", \"status\": \"closed\", \"success\": true}"
}

# 25) audit_log_action — create
AUDIT_LOG_ACTION_TASK = {
    "task_id": "if1_task_025",
    "description": "Write an audit entry for an update action on an incident",
    "function": "audit_log_action",
    "parameters": {
        "user_id": "205",
        "action": "update",
        "reference_type": "incident",
        "reference_id": "2004",
        "meta": "Changed priority from medium to high"
    },
    "expected_result": "{\"audit_id\": <str>, \"success\": true}"
}

# 26) get_incident — read
GET_INCIDENT_TASK = {
    "task_id": "if1_task_026",
    "description": "Read a single incident by ID",
    "function": "get_incident",
    "parameters": {
        "incident_id": "2016"
    },
    "expected_result": "Incident object including status, priority, category, assignments"
}
# 27) list_incidents — read
LIST_INCIDENTS_TASK = {
    "task_id": "if1_task_027",
    "description": "List open high-priority software incidents for dashboards",
    "function": "list_incidents",
    "parameters": {
        "status": "open",
        "priority": "high",
        "category": "software",
        "assigned_team": "L2",
        "affected_service": "3001",
        "created_since": "2025-09-20T00:00:00"
    },
    "expected_result": "Array of incident summaries matching the filters"
}

# 28) get_problem — read
GET_PROBLEM_TASK = {
    "task_id": "if1_task_028",
    "description": "Fetch a problem by ID with linked incidents",
    "function": "get_problem",
    "parameters": {
        "problem_id": "P-3001"
    },
    "expected_result": "Problem object with status and related links"
}

# 29) list_communications — read
LIST_COMMUNICATIONS_TASK = {
    "task_id": "if1_task_029",
    "description": "Retrieve all communications for an incident",
    "function": "list_communications",
    "parameters": {
        "incident_id": "2010"
    },
    "expected_result": "Array of communication records for the incident"
}


# All tasks for Interface 1
INTERFACE_1_TASKS = [
    ENTITIES_LOOKUP_TASK,
    CREATE_INCIDENT_TASK,
    LOG_INCIDENT_DETAILS_TASK,
    CATEGORIZE_INCIDENT_TASK,
    PRIORITIZE_INCIDENT_TASK,
    ASSIGN_INCIDENT_TASK,
    RECORD_DIAGNOSIS_WORKAROUND_TASK,
    ESCALATE_INCIDENT_TASK,
    CREATE_VENDOR_ENGAGEMENT_TASK,
    LINK_CHANGE_TO_INCIDENT_TASK,
    ADD_INCIDENT_COMMUNICATION_TASK,
    CLOSE_INCIDENT_TASK,
    CREATE_POST_INCIDENT_REVIEW_TASK,
    UPDATE_KNOWLEDGE_BASE_FROM_INCIDENT_TASK,
    CREATE_INCIDENT_FROM_MONITORING_EVENT_TASK,
    RECORD_TOOL_USAGE_TASK,
    RECORD_INCIDENT_SIMULATION_TASK,
    PROBLEM_CREATE_TASK,
    PROBLEM_UPDATE_TASK,
    PROBLEM_LINK_INCIDENT_TASK,
    PROBLEM_ADD_WORKAROUND_TASK,
    PROBLEM_RESOLVE_TASK,
    PROBLEM_CLOSE_TASK,
    AUDIT_LOG_ACTION_TASK,
    GET_INCIDENT_TASK,
    LIST_INCIDENTS_TASK,
    GET_PROBLEM_TASK,
    LIST_COMMUNICATIONS_TASK
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
