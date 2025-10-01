# Incident Management Domain - Aggregated Policy

## Overview

This document aggregates the rules, roles, SOPs, and governance for managing incidents, problems, changes, communications, knowledge, simulations, monitoring intake, tool usage, and audit within the Incident Management System (IMS). All procedures are **single-turn** (self-contained) and must halt with explicit error messaging if validations, authorizations, approvals, or integrations fail.

## Domain Description

The domain covers the end-to-end lifecycle: **identification → logging → categorization → prioritization → response/assignment → diagnosis/workaround → escalation → resolution/recovery → communication → closure → post-incident learning → knowledge updates → reporting**. Related processes include **problem management**, **change coordination**, **monitoring & alert intake**, **tool/automation usage**, **post-incident reviews**, and **audit**. All records and actions are captured in the **IMS** with immutable audit trails.

## Core Entities

### Incidents

* **Definition**: Unplanned interruption to an IT service or a reduction in service quality.
* **Lifecycle**: Detection → Logging → Categorization → Prioritization → In-Progress/Assignment → (Optional) Escalation/Vendor → Resolution → Closure.
* **Key Attributes**: `incident_id`, detection source (`user_report`, `monitoring_tool`, `automated_alert`), category (`hardware`, `software`, `security`, `performance`, `other`), priority (`low`, `medium`, `high`), severity (`low`, `medium`, `high`), status (`open`, `in_progress`, `escalated`, `pending_vendor`, `resolved`, `closed`), reporter, affected service, timestamps, resolver/closer.

### Change Requests

* **Definition**: Governance artifact to implement technical/structural changes that enable resolution.
* **Lifecycle**: Request → Approval → Implementation → Link to incident/problem → Review/Close.
* **Key Attributes**: `change_id`, summary, requester, approval status (`pending`, `approved`, `rejected`), approver, timestamps.

### Problem Tickets

* **Definition**: Underlying cause behind one or more incidents; managed distinctly but linked.
* **Lifecycle**: Create → Under Investigation → Workaround Available (known error) → Resolved → Closed.
* **Key Attributes**: `problem_id`, title, description, detection source, status, known_error, links (incidents/changes/KB), timestamps.

### Communications

* **Definition**: Status/notice updates associated with an incident.
* **Key Attributes**: `communication_id`, recipients group (`end_users`, `stakeholders`, `executives`, `IT_staff`), message, sender, timestamps.

### Monitoring Events

* **Definition**: Recorded alert/signal eligible for auto-creation of incidents.
* **Key Attributes**: `event_id`, detected service, source (`monitoring_tool`, `automated_alert`), alert type, severity, occurred/ingested at.

### Tool Usages & Simulations

* **Tool Usage**: `tool_used` in {`monitoring`, `root_cause_analysis`, `ITSM_service_desk`, `incident_response`, `AI_virtual_agent`, `AIOps`, `automation_script`}, action summary, executor, outcome.
* **Simulations**: Scenario, scope, simulated_by (Incident Manager), outcomes.

### Audit Trails

* **Definition**: Immutable record of actions across entities.
* **Key Attributes**: action (`identify`, `create`, `read`, `update`, `notify`, `escalate`, `resolve`, `close`, `review`, `kb_update`, `vendor_engagement`, `simulation`, `tool_use`, `link`), reference type, reference id, user, field deltas, timestamp.

## Service Level Management

### Service Level Agreements (SLAs)

* **Purpose**: Define response/resolution targets based on **priority** and **severity**.
* **Key Metrics**: Time to acknowledge, time to resolve, communication cadence.
* **Severity/Priority Mapping**: Apply policy definitions (low/medium/high) to drive targets and escalation.

### Escalation Procedures

* **Automatic**: Triggered by SLA breach thresholds or classification (e.g., high priority).
* **Manual**: When additional expertise/authority is required.
* **Targets**: `service_desk` → `L1` → `L2` → `L3` / `incident_manager` / `change_mgmt` / `facilities` / `devops`.

## Communication Management

### Communication Types

* **Internal** (teams), **External** (end users/stakeholders/executives), **Notifications** (status/ETA/resolution), **PIR outputs**.

### Channels

* **IMS communications record** (system of record), **email**, **meetings/briefings**. All messages must be recorded in IMS.

## Knowledge Management

### Knowledge Base Articles

* **Types**: Incident resolutions, workarounds (known errors), preventive measures.
* **Lifecycle**: Draft → Review/Approval → Published → Maintenance.
* **Linkage**: Incidents, problems, and changes link to relevant KB entries.

### Documentation Standards

* Structured, concise, actionable; redact sensitive data; version controlled.

## Quality Assurance

### Resolution Quality

* **First Contact Resolution**, **Mean Time to Resolve**, **Post-resolution validation**, **Stakeholder satisfaction** (where applicable).

### Process Compliance

* **Global Rules** enforced: validation-first, role-based authorization, SoD, audit logging, halt conditions, data minimization.

## Security and Compliance

### Data Protection

* **Confidentiality/Integrity/Availability**: Store only necessary context; avoid raw log dumps in audit/meta.
* **Access Control**: Role-based permissions (e.g., Incident Manager can close high-priority; reporter cannot approve/close where higher authority is required).

### Audit Requirements

* **Mandatory audit** for every create/update/approve/reject/close/notify/escalate/read where access controlled.
* **Retention** per organizational policy.

## Performance Metrics

### KPIs

* **MTTA/MTTR**, **Escalation rate**, **SLA compliance**, **Known error reuse rate** (workaround adoption), **Change success rate**.

### Reporting

* Cadence: **daily/weekly/monthly** dashboards; include trends, outliers, and PIR actions status.

## Continuous Improvement

### Post-Incident Reviews (PIR)

* Required for **high-priority**/major incidents.
* Outcomes: action items, KB updates, prevention standards, training needs.

### Process Optimization

* Periodic SOP review, automation/use of tools (AIOps/virtual agents), tuning of monitoring thresholds.

## Tools and Technology

### IMS (Ticketing System)

* **Authoritative record** for incidents/problems/changes/comms/simulations/audits.
* **Capabilities**: workflow enforcement, single-turn SOP execution, audit, reporting.

### Monitoring & Alerting

* Continuous monitoring; auto-creation criteria for incidents; integration with IMS for traceability.

### Knowledge System

* Central repository with linkage to incidents/problems/changes; searchable; versioned.

## Roles and Responsibilities

### Incident Manager

* Owns process enforcement, coordinates major incidents, leads PIRs, maintains KB.

### Service Desk Manager / Analysts (Service Desk, L1)

* First-line intake, logging, categorization, initial diagnosis, escalation as needed.

### L2 / L3 / DevOps / Facilities / Change Management

* Deeper triage and remediation; execute changes under governance; physical environment oversight (Facilities).

### End User

* Reports incidents via defined channels; consumes communications; validates service restoration.

## Training and Development

* **Initial**: SOPs, IMS usage, communication standards.
* **Ongoing**: Technology updates, root-cause skills, automation tools, PIR learnings.

## Integration Points

### Change Management

* Required for fixes that alter production; link change to incident/problem; approvals enforced.

### Problem Management

* Link incidents ↔ problems; record workarounds; transition to known error; resolve/close after validation.

### Monitoring Intake

* Convert qualified events to incidents with appropriate categorization/priority; notify service desk.

## Compliance and Governance

### Regulatory Alignment

* Align with industry frameworks (e.g., ITIL practices) and internal governance.
* Maintain **segregation of duties** (initiator ≠ approver/closer where required).

### Risk Management

* Assess change and incident risk; apply mitigations; track residual risk in PIRs.

---

### Standard Operating Procedures (Single-Turn, Halt on Error)

1. **Entities Lookup / Discovery**
   Validate `entity_type`, filters, requester → query IMS → return none/one/many (disambiguation).
   **Audit**: `action=identify` (entity discovery), store only entity type + filters used.

2. **Incident Identification**
   Validate reporter + inputs → confirm event qualifies → create incident `status=open`.
   **Audit**: `action=identify`, ref=incident.

3. **Incident Logging**
   Validate incident → append description, affected service, timestamp, initial diagnosis/workaround note.
   **Audit**: `action=create`, ref=incident.

4. **Incident Categorization**
   Validate incident + category enum → update category (+ subcategory).
   **Audit**: `action=update`, field=category.

5. **Incident Prioritization**
   Validate incident + priority + justification → update.
   **Audit**: `action=update`, field=priority.

6. **Initial Response & Assignment**
   Validate authorization, assign to team (`service_desk`, `L1`, `L2`, `L3`, `facilities`, `change_mgmt`, `devops`) → send acknowledgement (recorded as communication) → set `status=in_progress`.
   **Audit**: `action=update` (assignment) and `action=notify`.

7. **Diagnosis & Temporary Workaround**
   Validate inputs/role → record diagnostic steps and optional workaround details; mark workaround presence.
   **Audit**: `action=update`, field=diagnosis/workaround.

8. **Escalation**
   Validate path (e.g., `L2`, `L3`, `incident_manager`, `change_mgmt`, `facilities`, `devops`) + reason → update `status=escalated` and notify.
   **Audit**: `action=escalate`.

9. **Vendor Engagement**
   Validate incident + vendor context + contact method (`phone`, `email`, `vendor_portal`, `API`) → create vendor engagement, set `status=pending_vendor`.
   **Audit**: `action=vendor_engagement`.

10. **Change Coordination**
    Validate necessity and approvals (`approved` required) → link change to incident → execute per policy.
    **Audit**: `action=update`, field=change_link.

11. **Resolution & Recovery**
    Validate readiness + fix applied + service restored → set `status=resolved` with resolution summary & timestamp.
    **Audit**: `action=resolve`.

12. **Communication Updates**
    Validate incident + recipients group → record message (status/ETA/resolution).
    **Audit**: `action=notify`.

13. **Incident Closure**
    Preconditions: `status=resolved`; authority check (Incident Manager/Service Desk Manager for high priority); capture closure notes → set `status=closed`.
    **Audit**: `action=close`.

14. **Post-Incident Review (PIR)**
    Required for high-priority → Incident Manager documents timeline, factors, actions; link KB.
    **Audit**: `action=review`.

15. **Knowledge Base Update**
    Preconditions: incident closed → publish/update KB (resolutions, workarounds, prevention).
    **Audit**: `action=kb_update`.

16. **Monitoring & Alert Intake**
    Validate event + thresholds → auto-create incident with rules → notify service desk.
    **Audit**: `action=create` (source=monitoring).

17. **Tool & Automation Usage**
    Validate allowed tool → record action summary and outcome (no external execution here).
    **Audit**: `action=tool_use`.

18. **Incident Response Simulation**
    Validate role (Incident Manager) + scope → execute tabletop/drill → capture outcomes.
    **Audit**: `action=simulation`.

19. **Problem Management (Create/Update/Link/Workaround/Resolve/Close)**

    * Create with dedupe of active similar problems; optional link incidents.
    * Update allowed fields with field-level audit.
    * Link incident ↔ problem (bidirectional traceability).
    * Workaround: set `workaround_available` (known error) and publish to KB.
    * Resolve with validation evidence; Close after stability window.
      **Audit**: `create`, `update`, `link`, `kb_update`, `resolve`, `close`.

20. **Audit Trail Logging (Global)**
    Required for all governed actions; record minimal meta; halt on write failure.

---

*This aggregated policy is authoritative for IMS operations. Review at least quarterly or upon significant process/tooling change.*
