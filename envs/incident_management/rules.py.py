"""
Incident Management Domain Rules

This module contains all the rules and guidelines for the incident management domain
extracted strictly from the provided Incident management policy & SOPs document.
These rules define the business logic and constraints that govern the behavior of
the Incident Management System (IMS). All SOPs are single-turn and must halt with
explicit error messaging on failure.
"""

# ---------------------------------------------------------------------------
# Global / Cross-Cutting Rules 
# ---------------------------------------------------------------------------
GLOBAL_RULES = [
    "All Standard Operating Procedures (SOPs) are single-turn, self-contained, and completed in one interaction.",
    "If any internal tool or database call fails, halt and provide appropriate error messaging.",
    "Validation first: if required inputs are missing or invalid, halt with a specific error.",
    "Authorization & approvals: enforce role-based permissions and required approvals.",
    "Segregation of duties (SoD): the initiator of an incident record may not approve or close the same incident if closure requires higher authority.",
    "Logging & audit: every create, update, approve, reject, close, notify, or escalate must write an audit entry.",
    "Halt conditions: if inputs, authorization, or approvals are missing, or external calls fail—halt with precise messaging and, where appropriate, transfer_to_human.",
    "Data minimization: only record useful context in audit meta; do not store raw dumps of logs or sensitive data.",
    "Use only available tools; do not invent steps or call unavailable integrations.",
    "All incidents are recorded in the Incident Management System (IMS).",
]

# ---------------------------------------------------------------------------
# Incident Management Rules
# ---------------------------------------------------------------------------
INCIDENT_RULES = [
    "Creating incidents requires: reporter_id, client_id, title, description, category, severity, impact_level (component_id is optional).",
    "Before incident creation: validate reporter, client, and (if provided) component.",
    "Check for duplicate open incidents; if a duplicate exists, halt.",
    "On incident creation set timestamp and status=open, and link to client/component as applicable.",
    "Severity classification must follow: P1 complete outage/no workaround or enterprise-wide/regulatory/financial/high-priority client; P2 major degradation with workaround/multiple departments/SLA risk; P3 localized or moderate degradation with workaround; P4 minor or low-impact issue.",
    "Updating incident status/fields requires: incident_id, updated_by; optional new_status and field_updates.",
    "Apply updates with timestamp and user ID; return updated incident or halt if invalid/unauthorized.",
    "Escalations require: incident_id, target_user, reason, requested_by; verify incident and target user role.",
    "Resolving incidents requires: incident_id, resolved_by, resolution_summary; confirm impact mitigated, actions logged, and client informed; set status=resolved.",
    "Recording communications requires: incident_id, sender_user, recipient (user or group), delivery_method, message_content.",
    "Implementing workarounds requires: incident_id, description, effectiveness, implemented_by.",
    "Root cause analysis requires: incident_id, analysis_method, assigned_to; set RCA status=in_progress.",
    "Post-incident review requires: incident_id in resolved/closed state, scheduled_date (YYYY-MM-DD), and facilitator_user_id; set status=scheduled.",
]

# ---------------------------------------------------------------------------
# Change Management Rules 
# ---------------------------------------------------------------------------
CHANGE_RULES = [
    "Creating change requests requires: change_title, change_type, risk_level, requested_by (incident_id optional).",
    "Rollback requests require: change_id, justification, requested_by (incident_id optional).",
]



# ---------------------------------------------------------------------------
# Service Level / Escalation Rules
# ---------------------------------------------------------------------------
SLA_RULES = [
    "SLA creation requires: subscription_id, severity_level (P1|P2|P3|P4), response_time_minutes, resolution_time_hours (availability_target optional).",
    "Creating subscriptions requires: client_id, product_id, subscription_type (full_service|limited_service|trial|custom), service_level_tier (premium|standard|basic), start_date (YYYY-MM-DD) with optional end_date.",
    "Escalate when severity or SLA risk warrants elevation of response.",
]

# ---------------------------------------------------------------------------
# Communication Management Rules
# ---------------------------------------------------------------------------
COMMUNICATION_RULES = [
    "Allowed communication delivery methods: email, phone_call, chat, incident_portal_update, automated_notification.",
]

# ---------------------------------------------------------------------------
# Knowledge Management Rules
# ---------------------------------------------------------------------------
KNOWLEDGE_RULES = [
    "Creating knowledge base articles requires: title, content_type (troubleshooting|resolution_steps|prevention_guide|faq), category (incident_resolution|problem_management|change_management|troubleshooting|best_practice), author_id (incident_id and reviewer_user_id optional).",
    "New knowledge base articles start with status=draft.",
]

# ---------------------------------------------------------------------------
# Quality Assurance Rules 
# ---------------------------------------------------------------------------
QUALITY_RULES = [
    "Post-incident reviews evaluate timeline accuracy, communication effectiveness, and technical response ratings where recorded.",
]

# ---------------------------------------------------------------------------
# Security and Compliance Rules 
# ---------------------------------------------------------------------------
SECURITY_RULES = [
    "Permission validation uses: user role (incident_manager|technical_support|account_manager|executive|vendor_contact|system_administrator|client_contact) and status=active.",
    "Operations requiring elevated permissions must use the approval/check tool before proceeding.",
]

# ---------------------------------------------------------------------------
# Performance & Reporting Rules
# ---------------------------------------------------------------------------
PERFORMANCE_RULES = [
    "Recording performance metrics requires: incident_id (must be closed), metric_type (mean_time_to_detect|mean_time_to_acknowledge|mean_time_to_resolve|mean_time_between_failures|sla_breach_rate), and calculated_value_minutes (target_minutes optional).",
    "Generating incident reports requires: incident_id, report_type (executive_summary|postmortem_report|compliance_report|performance_dashboard|trend_analysis), and generated_by.",
]

# ---------------------------------------------------------------------------
# Integration & Tooling Rules
# ---------------------------------------------------------------------------
INTEGRATION_RULES = [
    "Use only approved internal tools that access the platform’s internal database (e.g., discovery, create/update entities, check_approval, log_audit_records, transfer_to_human).",
    "Do not access any external systems or resources; do not run background jobs, monitoring loops, or schedulers.",
    "If additional data is required and not provided, ask in the same turn; if still missing, halt.",
]

# ---------------------------------------------------------------------------
# Aggregations & Helpers
# ---------------------------------------------------------------------------
ALL_RULES = (
    GLOBAL_RULES +
    INCIDENT_RULES +
    CHANGE_RULES +
    SLA_RULES +
    COMMUNICATION_RULES +
    KNOWLEDGE_RULES +
    QUALITY_RULES +
    SECURITY_RULES +
    PERFORMANCE_RULES +
    INTEGRATION_RULES
)

RULE_CATEGORIES = {
    "global": GLOBAL_RULES,
    "incident": INCIDENT_RULES,
    "change": CHANGE_RULES,
    "sla": SLA_RULES,
    "communication": COMMUNICATION_RULES,
    "knowledge": KNOWLEDGE_RULES,
    "quality": QUALITY_RULES,
    "security": SECURITY_RULES,
    "performance": PERFORMANCE_RULES,
    "integration": INTEGRATION_RULES,
}

def get_rules_by_category(category: str):
    """Return rules for a specific category; empty list if unknown."""
    return RULE_CATEGORIES.get(category, [])

def get_all_rules():
    """Return the full, concatenated rules list."""
    return ALL_RULES

def get_rule_count() -> int:
    """Return the total number of rules."""
    return len(ALL_RULES)

def search_rules(keyword: str):
    """Return rules containing the case-insensitive keyword."""
    key = (keyword or "").lower()
    return [r for r in ALL_RULES if key in r.lower()]
