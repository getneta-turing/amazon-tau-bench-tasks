"""
Interface 5 Tasks - Incident Management Domain (Synonym Functions)

This module mirrors the Interface 1 task implementations but renames each task's
'function' to the Interface 5 API names (synonyms). Parameters and expected
results remain the same.
"""

# NOTE:
# - IDs are strings.
# - Timestamps are ISO-8601 strings when present.
# - Enum values follow the Incident Management Policy & SOPs.


# 1) retrieve_entities 
RETRIEVE_ENTITIES_TASK = {
    "task_id": "if5_task_001",
    "description": "Lookup a user by email for verification",
    "function": "retrieve_entities",
    "parameters": {
        "entity_type": "user",
        "filters": {"email": "sda.jane.doe@example.com"},
        "requester_id": "101"
    },
    "expected_result": "Zero, one, or many users matching the email"
}

# 2) file_incident 
FILE_INCIDENT_TASK = {
    "task_id": "if5_task_002",
    "description": "Create a new incident reported by a user",
    "function": "file_incident",
    "parameters": {
        "reporter_id": "101",
        "detection_source": "user_report",
        "initial_description": "Email service is intermittently failing for multiple users."
    },
    "expected_result": "{\"incident_id\": <str>, \"status\": \"open\", \"success\": true}"
}

# 3) note_incident_details
NOTE_INCIDENT_DETAILS_TASK = {
    "task_id": "if5_task_003",
    "description": "Append core details to an existing incident",
    "function": "note_incident_details",
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

# 4) group_incident 
GROUP_INCIDENT_TASK = {
    "task_id": "if5_task_004",
    "description": "Categorize an incident as a software issue",
    "function": "group_incident",
    "parameters": {
        "incident_id": "2002",
        "category": "software",
        "sub_category": "email_delivery"
    },
    "expected_result": "{\"incident_id\": \"2002\", \"category\": \"software\", \"success\": true}"
}

# 5) grade_incident_priority 
GRADE_INCIDENT_PRIORITY_TASK = {
    "task_id": "if5_task_005",
    "description": "Set incident priority to high with justification",
    "function": "grade_incident_priority",
    "parameters": {
        "incident_id": "2003",
        "priority": "high",
        "justification": "Affects most end users; business-critical service impact."
    },
    "expected_result": "{\"incident_id\": \"2003\", \"priority\": \"high\", \"success\": true}"
}

# 6) designate_incident 
DESIGNATE_INCIDENT_TASK = {
    "task_id": "if5_task_006",
    "description": "Assign the incident to L2 and acknowledge",
    "function": "designate_incident",
    "parameters": {
        "incident_id": "2004",
        "assigned_team": "L2",
        "responder_user_id": "205",
        "communication_message": "Incident acknowledged by L2. Investigation started."
    },
    "expected_result": "{\"incident_id\": \"2004\", \"status\": \"in_progress\", \"assigned_team\": \"L2\", \"success\": true}"
}

# 7) record_triage_workaround 
RECORD_TRIAGE_WORKAROUND_TASK = {
    "task_id": "if5_task_007",
    "description": "Record diagnostic steps and temporary workaround",
    "function": "record_triage_workaround",
    "parameters": {
        "incident_id": "2005",
        "diagnostic_steps_summary": "Checked MX-2 queues; identified burst traffic from misconfigured agent.",
        "workaround_applied": True,
        "responder_user_id": "205",
        "workaround_details": "Throttled offending agent; reduced inbound queue size."
    },
    "expected_result": "Incident updated with diagnosis and workaround details"
}

# 8) escalate_ticket 
ESCALATE_TICKET_TASK = {
    "task_id": "if5_task_008",
    "description": "Escalate incident to L3 specialists",
    "function": "escalate_ticket",
    "parameters": {
        "incident_id": "2006",
        "escalated_to": "L3",
        "reason_for_escalation": "Deep mail routing logic issue suspected.",
        "escalated_by_user_id": "205"
    },
    "expected_result": "{\"incident_id\": \"2006\", \"status\": \"escalated\", \"escalated_to\": \"L3\", \"success\": true}"
}

# 9) log_vendor_engagement 
LOG_VENDOR_ENGAGEMENT_TASK = {
    "task_id": "if5_task_009",
    "description": "Engage vendor via portal and mark incident pending_vendor",
    "function": "log_vendor_engagement",
    "parameters": {
        "incident_id": "2007",
        "vendor_name": "MailCloud Inc.",
        "contact_method": "vendor_portal",
        "vendor_ticket_reference": "MC-CASE-8891",
        "initiated_by_user_id": "310"
    },
    "expected_result": "{\"incident_id\": \"2007\", \"vendor_engagement_id\": <str>, \"status\": \"pending_vendor\", \"success\": true}"
}

# 10) attach_change_to_incident
ATTACH_CHANGE_TO_INCIDENT_TASK = {
    "task_id": "if5_task_010",
    "description": "Record a change coordination reference for the incident",
    "function": "attach_change_to_incident",
    "parameters": {
        "incident_id": "2008",
        "change_summary": "Reconfigure MX-2 routing policy and deploy hotfix.",
        "requested_by": "change_mgmt",
        "approval_record_id": "A-555"
    },
    "expected_result": "{\"incident_id\": \"2008\", \"change_link_id\": <str>, \"success\": true}"
}

# 11) conclude_incident_resolution 
CONCLUDE_INCIDENT_RESOLUTION_TASK = {
    "task_id": "if5_task_011",
    "description": "Resolve the incident after permanent fix",
    "function": "conclude_incident_resolution",
    "parameters": {
        "incident_id": "2009",
        "resolution_summary": "Applied configuration hotfix; queues normalized.",
        "resolved_by_user_id": "401",
        "resolution_timestamp": "2025-10-01T01:45:00"
    },
    "expected_result": "{\"incident_id\": \"2009\", \"status\": \"resolved\", \"success\": true}"
}

# 12) add_incident_update 
ADD_INCIDENT_UPDATE_TASK = {
    "task_id": "if5_task_012",
    "description": "Post a stakeholder update on incident progress",
    "function": "add_incident_update",
    "parameters": {
        "incident_id": "2010",
        "message_text": "Root cause identified; mitigation in progress. Next update in 30 minutes.",
        "recipients_group": "stakeholders",
        "sent_by_user_id": "205"
    },
    "expected_result": "{\"communication_id\": <str>, \"incident_id\": \"2010\", \"success\": true}"
}

# 13) close_out_incident
CLOSE_OUT_INCIDENT_TASK = {
    "task_id": "if5_task_013",
    "description": "Close a resolved incident with closure notes",
    "function": "close_out_incident",
    "parameters": {
        "incident_id": "2011",
        "closed_by_user_id": "102",
        "closure_notes": "Monitored for 2 hours; stable with normal latency."
    },
    "expected_result": "{\"incident_id\": \"2011\", \"status\": \"closed\", \"success\": true}"
}

# 14) create_pir_record 
CREATE_PIR_RECORD_TASK = {
    "task_id": "if5_task_014",
    "description": "Create a PIR for a high-priority incident",
    "function": "create_pir_record",
    "parameters": {
        "incident_id": "2012",
        "review_notes": "Timeline captured; contributing factors include misconfigured agent.",
        "conducted_by_user_id": "100"
    },
    "expected_result": "{\"review_id\": <str>, \"incident_id\": \"2012\", \"success\": true}"
}

# 15) apply_incident_kb_update 
APPLY_INCIDENT_KB_UPDATE_TASK = {
    "task_id": "if5_task_015",
    "description": "Publish KB update with resolution and preventive actions",
    "function": "apply_incident_kb_update",
    "parameters": {
        "incident_id": "2013",
        "kb_update_notes": "Add MX queue monitoring threshold and agent config validation checklist.",
        "submitted_by_user_id": "100"
    },
    "expected_result": "{\"kb_entry_id\": <str>, \"linked_incident_id\": \"2013\", \"success\": true}"
}

# 16) derive_incident_from_monitoring 
DERIVE_INCIDENT_FROM_MONITORING_TASK = {
    "task_id": "if5_task_016",
    "description": "Create an incident from an existing monitoring event",
    "function": "derive_incident_from_monitoring",
    "parameters": {
        "monitoring_event_id": "EVT-9001",
        "detected_service": "3002",
        "alert_details": "CPU utilization sustained over 95% for 10 minutes."
    },
    "expected_result": "{\"incident_id\": <str>, \"source\": \"monitoring\", \"status\": \"open\", \"success\": true}"
}

# 17) register_tool_usage
REGISTER_TOOL_USAGE_TASK = {
    "task_id": "if5_task_017",
    "description": "Log the use of an AIOps correlation run on an incident",
    "function": "register_tool_usage",
    "parameters": {
        "incident_id": "2014",
        "tool_used": "AIOps",
        "action_summary": "Correlated spikes to deployment window; suggested rollback.",
        "executed_by": "205"
    },
    "expected_result": "{\"tool_use_id\": <str>, \"incident_id\": \"2014\", \"success\": true}"
}

# 18) register_incident_simulation 
REGISTER_INCIDENT_SIMULATION_TASK = {
    "task_id": "if5_task_018",
    "description": "Record a simulated incident drill for the core email service",
    "function": "register_incident_simulation",
    "parameters": {
        "scenario_name": "Email outage tabletop",
        "simulated_by_user_id": "100",
        "scope": "email_service"
    },
    "expected_result": "{\"simulation_id\": <str>, \"success\": true}"
}

# 19) create_problem 
CREATE_PROBLEM_TASK = {
    "task_id": "if5_task_019",
    "description": "Create a problem for recurring MX queue backlogs",
    "function": "create_problem",
    "parameters": {
        "problem_title": "Recurring MX queue backlog",
        "description": "Multiple incidents with queue saturation during peak hours.",
        "detection_source": "monitoring_tool",
        "created_by_user_id": "401",
        "related_incident_ids": ["2005", "2007"]
    },
    "expected_result": "{\"problem_id\": <str>, \"status\": \"open\", \"success\": true}"
}

# 20) update_problem 
UPDATE_PROBLEM_TASK = {
    "task_id": "if5_task_020",
    "description": "Update a problem with refined scope and assignee",
    "function": "update_problem",
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

# 21) link_problem_incident 
LINK_PROBLEM_INCIDENT_TASK = {
    "task_id": "if5_task_021",
    "description": "Link an incident to an existing problem",
    "function": "link_problem_incident",
    "parameters": {
        "problem_id": "P-3001",
        "incident_id": "2015",
        "linked_by_user_id": "405"
    },
    "expected_result": "{\"problem_id\": \"P-3001\", \"incident_id\": \"2015\", \"success\": true}"
}

# 22) add_problem_workaround 
ADD_PROBLEM_WORKAROUND_TASK = {
    "task_id": "if5_task_022",
    "description": "Add a workaround to the problem and publish to KB",
    "function": "add_problem_workaround",
    "parameters": {
        "problem_id": "P-3002",
        "workaround_summary": "Temporarily reduce retry rate; auto-drain queues nightly.",
        "added_by_user_id": "405"
    },
    "expected_result": "{\"problem_id\": \"P-3002\", \"status\": \"workaround_available\", \"kb_link_id\": <str>, \"success\": true}"
}

# 23) resolve_problem 
RESOLVE_PROBLEM_TASK = {
    "task_id": "if5_task_023",
    "description": "Resolve the problem with a validated permanent fix",
    "function": "resolve_problem",
    "parameters": {
        "problem_id": "P-3003",
        "permanent_fix_summary": "Policy engine patch v2.1; adaptive retry backoff.",
        "validation_evidence": "Post-patch monitoring shows stable queues over 7 days.",
        "resolved_by_user_id": "405"
    },
    "expected_result": "{\"problem_id\": \"P-3003\", \"status\": \"resolved\", \"success\": true}"
}

# 24) close_problem 
CLOSE_PROBLEM_TASK = {
    "task_id": "if5_task_024",
    "description": "Close a resolved problem after stability window",
    "function": "close_problem",
    "parameters": {
        "problem_id": "P-3003",
        "closed_by_user_id": "100",
        "closure_notes": "Stable over 14 days; no reoccurrences."
    },
    "expected_result": "{\"problem_id\": \"P-3003\", \"status\": \"closed\", \"success\": true}"
}

# 25) register_audit_event 
REGISTER_AUDIT_EVENT_TASK = {
    "task_id": "if5_task_025",
    "description": "Write an audit entry for an update action on an incident",
    "function": "register_audit_event",
    "parameters": {
        "user_id": "205",
        "action": "update",
        "reference_type": "incident",
        "reference_id": "2004",
        "meta": "Changed priority from medium to high"
    },
    "expected_result": "{\"audit_id\": <str>, \"success\": true}"
}

# 26) get_incident_record 
GET_INCIDENT_RECORD_TASK = {
    "task_id": "if5_task_026",
    "description": "Read a single incident by ID",
    "function": "get_incident_record",
    "parameters": {
        "incident_id": "2016"
    },
    "expected_result": "Incident object including status, priority, category, assignments"
}

# 27) query_incidents 
QUERY_INCIDENTS_TASK = {
    "task_id": "if5_task_027",
    "description": "List open high-priority software incidents for dashboards",
    "function": "query_incidents",
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

# 28) get_problem_record 
GET_PROBLEM_RECORD_TASK = {
    "task_id": "if5_task_028",
    "description": "Fetch a problem by ID with linked incidents",
    "function": "get_problem_record",
    "parameters": {
        "problem_id": "P-3001"
    },
    "expected_result": "Problem object with status and related links"
}

# 29) list_incident_communications 
LIST_INCIDENT_COMMUNICATIONS_TASK = {
    "task_id": "if5_task_029",
    "description": "Retrieve all communications for an incident",
    "function": "list_incident_communications",
    "parameters": {
        "incident_id": "2010"
    },
    "expected_result": "Array of communication records for the incident"
}


INTERFACE_5_TASKS = [
    RETRIEVE_ENTITIES_TASK,
    FILE_INCIDENT_TASK,
    NOTE_INCIDENT_DETAILS_TASK,
    GROUP_INCIDENT_TASK,
    GRADE_INCIDENT_PRIORITY_TASK,
    DESIGNATE_INCIDENT_TASK,
    RECORD_TRIAGE_WORKAROUND_TASK,
    ESCALATE_TICKET_TASK,
    LOG_VENDOR_ENGAGEMENT_TASK,
    ATTACH_CHANGE_TO_INCIDENT_TASK,
    CONCLUDE_INCIDENT_RESOLUTION_TASK,
    ADD_INCIDENT_UPDATE_TASK,
    CLOSE_OUT_INCIDENT_TASK,
    CREATE_PIR_RECORD_TASK,
    APPLY_INCIDENT_KB_UPDATE_TASK,
    DERIVE_INCIDENT_FROM_MONITORING_TASK,
    REGISTER_TOOL_USAGE_TASK,
    REGISTER_INCIDENT_SIMULATION_TASK,
    CREATE_PROBLEM_TASK,
    UPDATE_PROBLEM_TASK,
    LINK_PROBLEM_INCIDENT_TASK,
    ADD_PROBLEM_WORKAROUND_TASK,
    RESOLVE_PROBLEM_TASK,
    CLOSE_PROBLEM_TASK,
    REGISTER_AUDIT_EVENT_TASK,
    GET_INCIDENT_RECORD_TASK,
    QUERY_INCIDENTS_TASK,
    GET_PROBLEM_RECORD_TASK,
    LIST_INCIDENT_COMMUNICATIONS_TASK,
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
    """Get the total number of Interface 5 tasks"""
    return len(INTERFACE_5_TASKS)
