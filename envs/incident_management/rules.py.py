"""
Incident Management Domain Rules

This module contains all the rules and guidelines for the incident management domain
extracted from the aggregated policy and SOPs. These rules define the business logic and
constraints that govern the behavior of the Incident Management System (IMS).
All SOPs are single-turn and must halt with explicit error messaging on failure.
"""

# ---------------------------------------------------------------------------
# Global / Cross-Cutting Rules (apply to all entities and SOPs)
# ---------------------------------------------------------------------------
GLOBAL_RULES = [
    "Validation-first: If required inputs are missing or invalid, halt with a precise error.",
    "Authorization & approvals: Enforce role-based permissions and required approvals for each action.",
    "Segregation of duties: The initiator of an item cannot approve or close it when higher authority is required.",
    "Logging & audit: Every create, read (when access-controlled), update, notify, escalate, resolve, close, review, kb_update, vendor_engagement, simulation, tool_use, or link must write an audit entry.",
    "Halt conditions: If inputs, authorization, approvals are missing, or an external call fails, halt with specific messaging (and transfer to human where appropriate).",
    "Data minimization: Record only useful context in audit meta; no raw dumps of logs or sensitive data.",
    "Single-turn execution: Each SOP is self-contained and must complete in one interaction.",
    "Use only approved tools and IMS: Do not invent steps or call unavailable integrations.",
    "Immutable traceability: Preserve end-to-end traceability across incidents, problems, changes, communications, monitoring events, simulations, tool usage, and audits.",
]

# ---------------------------------------------------------------------------
# Incident Management Rules
# ---------------------------------------------------------------------------
INCIDENT_RULES = [
    "Each incident must have a unique incident_id and created_at timestamp.",
    "Allowed incident statuses: open, in_progress, escalated, pending_vendor, resolved, closed.",
    "Allowed categories: hardware, software, security, performance, other.",
    "Allowed priorities: low, medium, high.",
    "Detection sources: user_report, monitoring_tool, automated_alert.",
    "Creation (identification) sets status=open and must write an audit action=identify.",
    "Logging must capture description, affected service (if known), timestamp, and optional initial diagnosis/workaround note.",
    "Categorization must validate the category enum and write audit action=update (field=category).",
    "Prioritization must validate the priority enum, include justification, and write audit action=update (field=priority).",
    "Initial response & assignment must set status=in_progress, create an acknowledgement communication, and write audit actions update (assignment) and notify.",
    "Diagnosis & temporary workaround must record diagnostic steps; if workaround exists, store details and write audit action=update (field=diagnosis/workaround).",
    "Escalation must validate the target team (L2, L3, incident_manager, change_mgmt, facilities, devops), update status=escalated, and write audit action=escalate.",
    "Vendor engagement sets incident status=pending_vendor and records vendor reference; write audit action=vendor_engagement.",
    "Resolution must verify service restoration, record the resolution summary and timestamp, set status=resolved, and write audit action=resolve.",
    "Closure requires status=resolved and appropriate authority (e.g., Incident Manager/Service Desk Manager for high priority); set status=closed and write audit action=close.",
    "Communications must specify recipients group (end_users, stakeholders, executives, IT_staff) and are recorded in IMS with audit action=notify.",
    "Incidents auto-created from monitoring events must reference the source event and write audit action=create (source=monitoring).",
]

# ---------------------------------------------------------------------------
# Change Management Rules (as used within incident coordination)
# ---------------------------------------------------------------------------
CHANGE_RULES = [
    "Changes linked to incidents must be recorded via a change_request with approval status (pending, approved, rejected).",
    "Execution of a change that alters production requires prior approval per policy.",
    "Change linkage to incidents/problems must be auditable (action=update, field=change_link).",
    "Change records must include requester, summary, timestamps, and approver (when approved).",
    "Post-implementation verification is required before considering resolution dependent on the change.",
]

# ---------------------------------------------------------------------------
# Problem Management Rules
# ---------------------------------------------------------------------------
PROBLEM_RULES = [
    "Problems represent underlying causes and are distinct from incidents but must maintain bidirectional links.",
    "Problem statuses: open, under_investigation, workaround_available (known_error), resolved, closed.",
    "Creating a problem should avoid duplicates of active similar problems (dedupe check).",
    "Linking incidents to problems must be unique per pair and auditable (action=link).",
    "Workarounds recorded on problems set status=workaround_available and must be published to the knowledge base (action=kb_update).",
    "Resolving a problem requires permanent fix details and validation evidence; write audit action=resolve.",
    "Closing a problem requires prior resolution and stability verification; write audit action=close.",
]

# ---------------------------------------------------------------------------
# Service Level / Escalation Rules (policy-aligned, non-timebox specific)
# ---------------------------------------------------------------------------
SLA_RULES = [
    "SLA targets derive from priority and severity definitions and guide response, communication cadence, and escalation.",
    "Automatic escalation may be triggered by SLA breach conditions or high priority classification.",
    "Manual escalation is permitted when additional expertise or authority is required.",
    "Communication cadence during active incidents must follow SLA guidance and be recorded in IMS.",
]

# ---------------------------------------------------------------------------
# Communication Management Rules
# ---------------------------------------------------------------------------
COMMUNICATION_RULES = [
    "All incident communications must be recorded in IMS with recipients group and message content.",
    "Messages must be concise, accurate, and appropriate for the audience (end_users, stakeholders, executives, IT_staff).",
    "Status changes (acknowledgement, escalation, resolution, closure) require corresponding communications where applicable.",
    "Post-resolution communications summarize resolution and verification of service restoration.",
    "Do not store sensitive information or raw logs in communications; follow data minimization.",
]

# ---------------------------------------------------------------------------
# Knowledge Management Rules
# ---------------------------------------------------------------------------
KNOWLEDGE_RULES = [
    "KB entries support incident resolution, workarounds (known errors), and preventive measures.",
    "KB lifecycle: draft → review/approval → published → maintenance; status must be tracked (draft, published, archived).",
    "Workarounds promoted to known error must have published KB entries linked to problems/incidents.",
    "KB updates from incidents must occur after closure and be auditable (action=kb_update).",
    "KB content must be structured, searchable, minimally sensitive, and version-controlled.",
]

# ---------------------------------------------------------------------------
# Quality Assurance Rules
# ---------------------------------------------------------------------------
QUALITY_RULES = [
    "Resolution quality must be verified before closure (service restoration confirmed).",
    "Post-incident reviews (PIR) are mandatory for high-priority/major incidents and must capture timeline, factors, and actions.",
    "Dashboards and reports must track MTTA/MTTR, escalation rates, SLA compliance, and PIR action completion.",
    "Process adherence (validation-first, SoD, audit) is monitored and enforced.",
]

# ---------------------------------------------------------------------------
# Security and Compliance Rules
# ---------------------------------------------------------------------------
SECURITY_RULES = [
    "Apply role-based access control to all IMS reads/writes; access-controlled reads may require audit logging.",
    "Protect confidentiality, integrity, and availability of IMS data; avoid storing raw sensitive data in audit/meta.",
    "Maintain immutable audit trails with minimal but sufficient context for every governed action.",
    "Retain records per policy; ensure backups and recovery meet compliance requirements.",
]

# ---------------------------------------------------------------------------
# Performance & Reporting Rules
# ---------------------------------------------------------------------------
PERFORMANCE_RULES = [
    "Key KPIs include MTTA, MTTR, escalation rate, SLA compliance, workaround reuse/known error effectiveness, and change success rate.",
    "Reports are produced on a defined cadence (daily/weekly/monthly) and include trends and outliers.",
    "PIR action items are tracked to completion and reported.",
]

# ---------------------------------------------------------------------------
# Integration & Tooling Rules
# ---------------------------------------------------------------------------
INTEGRATION_RULES = [
    "IMS is the authoritative system of record; all integrations (monitoring, knowledge, change, tooling) must maintain traceability.",
    "Monitoring events that meet criteria can auto-create incidents with source linkage.",
    "Tool/automation usage (monitoring, RCA, ITSM_service_desk, incident_response, AI_virtual_agent, AIOps, automation_script) must be recorded with outcome and audit action=tool_use.",
    "Simulations (test drills) require Incident Manager authorization and must record outcomes with audit action=simulation.",
]

# ---------------------------------------------------------------------------
# Aggregations & Helpers
# ---------------------------------------------------------------------------
ALL_RULES = (
    GLOBAL_RULES +
    INCIDENT_RULES +
    CHANGE_RULES +
    PROBLEM_RULES +
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
    "problem": PROBLEM_RULES,
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
