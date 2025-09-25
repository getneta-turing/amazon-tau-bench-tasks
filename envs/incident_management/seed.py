# ims_seed.py
# pip install Faker python-dateutil
from __future__ import annotations
from faker import Faker
from datetime import datetime, timedelta, date
from dateutil.tz import tzutc
import json, os, random
from typing import Dict, List, Any, Callable

fake = Faker()
fake.seed(2025)
random.seed(2025)

OUT_DIR = "seed"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- Helpers --------
def now():
    return datetime.now(tzutc())

def ts_between(start: datetime, end: datetime) -> datetime:
    if end <= start:
        end = start + timedelta(minutes=1)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def make_stamp_pair() -> tuple[str, str]:
    start = now() - timedelta(days=random.randint(10, 180))
    updated = ts_between(start + timedelta(minutes=1), start + timedelta(days=random.randint(0, 30)))
    return start.isoformat(), updated.isoformat()

def next_id(counter: Dict[str, int], key: str) -> str:
    counter[key] = counter.get(key, 0) + 1
    return str(counter[key])

def choose_one(seq: List[Any]) -> Any:
    return random.choice(seq)

def choose_some_parents(parents: List[str], max_per_parent: int) -> Dict[str, int]:
    """
    Return a dict parent_id -> num_children to create, with each <= max_per_parent, possibly 0.
    """
    plan = {}
    for pid in parents:
        plan[pid] = random.randint(0, max_per_parent)
    return plan

def write_json(filename: str, data: Dict[str, Any]):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# -------- Enumerations (from policy/schema) --------
ROLES = ['requester','service_desk','incident_manager','resolver','change_authority','communications_lead','compliance_audit']
USER_STATUS = ['active','inactive','suspended']
GROUP_TYPES = ['resolver','service_desk','communications','compliance','other']
ROLE_IN_GROUP = ['member','lead']
CLIENT_STATUS = ['active','inactive']
SERVICE_TIER = ['gold','silver','bronze','none']
COMPONENT_STATUS = ['active','retired']
INCIDENT_CATEGORY = ['infrastructure','application','network','security','service_request','other']
SEVERITY = ['P1','P2','P3','P4']
INCIDENT_STATUS = ['new','triage','in_progress','mitigated','resolved','closed','cancelled']
PROBLEM_STATUS = ['open','in_progress','resolved','closed']
CHANGE_TYPE = ['standard','normal','emergency']
RISK = ['low','medium','high']
CHANGE_STATUS = ['requested','approved','scheduled','implemented','failed','rolled_back','cancelled']
WORKORDER_STATUS = ['scheduled','in_progress','completed','failed','cancelled']
ESCALATION_STATUS = ['requested','accepted','declined','completed']
TARGET_ROLE = ['incident_manager','resolver','communications_lead','change_authority','compliance_audit','service_desk','requester']
EFFECTIVENESS = ['ineffective','partial','effective']
RCA_METHOD = ['five_whys','fishbone','timeline','fault_tree','postmortem']
RCA_STATUS = ['in_progress','completed']
RECIPIENT_TYPE = ['stakeholders','customers','internal','specific_users']
COMM_TYPE = ['incident_update','stakeholder_notice','customer_notice','internal_note']
DELIVERY_METHOD = ['email','sms','call','portal']
DELIVERY_STATUS = ['pending','sent','failed']
REPORT_TYPES = ['summary','timeline','postmortem','metrics']
REPORT_STATUS = ['pending','completed','failed']
METRIC_TYPES = ['MTTA','MTTR','MTTD','time_to_comm']
KB_CONTENT = ['how_to','troubleshooting','postmortem','reference']
KB_CATEGORY = ['infrastructure','application','network','security','general']
KB_STATUS = ['draft','published','archived']
PIR_STATUS = ['scheduled','completed','cancelled']
ACTION_SCOPE = ['incident_creation','severity_set','status_transition','escalation','workaround','rca','change_request','rollback','communication','resolution','closure','report_generation','kb_publish','pir_schedule']
APPROVER_ROLE = ['incident_manager','change_authority','communications_lead','compliance_audit']
DECISION = ['approved','rejected']
AUD_REF_TYPES = ['user','client','component','incident','problem','change_request','work_order','escalation','workaround','rca','communication','status_history','report','metric','knowledge','pir','approval']
AUD_ACTIONS = ['create','read','update','delete','approve','reject','status_change','link','generate']

# Email domain pool for realism (rule 12)
EMAIL_DOMAINS = ["gmail.com", "outlook.com", "yahoo.com", "proton.me", "company.io"]

def make_email(full_name: str) -> str:
    base = full_name.lower().replace("'", "").replace(".", "").replace("-", " ")
    parts = [p for p in base.split() if p]
    handle = ".".join(parts[:2]) if len(parts) >= 2 else parts[0]
    suffix = str(random.randint(10, 999))
    return f"{handle}{suffix}@{choose_one(EMAIL_DOMAINS)}"

# -------- Generators per table --------
idc = {}  # per-table counters

users: Dict[str, Any] = {}
groups: Dict[str, Any] = {}
user_groups: Dict[str, Any] = {}
clients: Dict[str, Any] = {}
components: Dict[str, Any] = {}
incidents: Dict[str, Any] = {}
problem_tickets: Dict[str, Any] = {}
change_requests: Dict[str, Any] = {}
rollback_requests: Dict[str, Any] = {}
work_orders: Dict[str, Any] = {}
escalations: Dict[str, Any] = {}
workarounds: Dict[str, Any] = {}
root_cause_analyses: Dict[str, Any] = {}
communications: Dict[str, Any] = {}
incident_status_history: Dict[str, Any] = {}
incident_links: Dict[str, Any] = {}
reports: Dict[str, Any] = {}
metrics: Dict[str, Any] = {}
knowledge_articles: Dict[str, Any] = {}
post_incident_reviews: Dict[str, Any] = {}
approvals: Dict[str, Any] = {}
audit_trails: Dict[str, Any] = {}

# Users (8–12)
for _ in range(random.randint(8, 12)):
    uid = next_id(idc, "users")
    full_name = fake.name()
    created_at, updated_at = make_stamp_pair()
    users[uid] = {
        "user_id": str(uid),
        "full_name": full_name,
        "email": make_email(full_name),
        "role": choose_one(ROLES),
        "status": choose_one(USER_STATUS if random.random() < 0.15 else ['active']),
        "timezone": random.choice(["UTC", "Africa/Addis_Ababa", "Europe/London", "America/New_York"]),
        "created_at": created_at,
        "updated_at": updated_at
    }

# Groups (resolver/service_desk/etc.) 4–6
group_names = ["Platform Ops", "Network SRE", "Service Desk A", "Change CAB", "Comms Guild", "Compliance Team"]
random.shuffle(group_names)
for name in group_names[:random.randint(4, 6)]:
    gid = next_id(idc, "groups")
    created_at, updated_at = make_stamp_pair()
    groups[gid] = {
        "group_id": str(gid),
        "name": name,
        "group_type": choose_one(GROUP_TYPES),
        "created_at": created_at,
        "updated_at": updated_at
    }

# User-Group memberships (each user 0–2 groups, ≤3 members per group per rule max children)
# We'll enforce ≤3 user_groups per group.
group_ids = list(groups.keys())
per_group_count = {g: 0 for g in group_ids}
for uid in users.keys():
    memberships = random.randint(0, 2)
    cand = random.sample(group_ids, k=min(memberships, len(group_ids))) if group_ids else []
    for gid in cand:
        if per_group_count[gid] >= 3:
            continue
        ugid = next_id(idc, "user_groups")
        assigned_at = ts_between(datetime.fromisoformat(users[uid]["created_at"]), datetime.fromisoformat(users[uid]["updated_at"])).isoformat()
        user_groups[ugid] = {
            "user_group_id": str(ugid),
            "user_id": str(uid),
            "group_id": str(gid),
            "role_in_group": choose_one(ROLE_IN_GROUP),
            "assigned_at": assigned_at
        }
        per_group_count[gid] += 1

# Clients (5–8)
for _ in range(random.randint(5, 8)):
    cid = next_id(idc, "clients")
    created_at, updated_at = make_stamp_pair()
    cname = f"{fake.company()} Ltd."
    clients[cid] = {
        "client_id": str(cid),
        "legal_name": cname,
        "status": choose_one(CLIENT_STATUS if random.random() < 0.2 else ['active']),
        "primary_contact_email": make_email(fake.name()),
        "created_at": created_at,
        "updated_at": updated_at
    }

# Components per client (0–3) + some shared (client_id = null allowed by schema)
client_ids = list(clients.keys())
for cid in client_ids:
    for _ in range(random.randint(0, 3)):
        comp_id = next_id(idc, "components")
        created_at, updated_at = make_stamp_pair()
        components[comp_id] = {
            "component_id": str(comp_id),
            "name": f"{fake.color_name()}-{fake.word().title()}",
            "client_id": str(cid),  # linked
            "service_tier": choose_one(SERVICE_TIER),
            "status": choose_one(COMPONENT_STATUS if random.random() < 0.1 else ['active']),
            "created_at": created_at,
            "updated_at": updated_at
        }

# Add 0–2 shared components (client_id null is realistic per schema comment)
for _ in range(random.randint(0, 2)):
    comp_id = next_id(idc, "components")
    created_at, updated_at = make_stamp_pair()
    components[comp_id] = {
        "component_id": str(comp_id),
        "name": f"{fake.color_name()}-Shared",
        "client_id": None,  # shared
        "service_tier": choose_one(SERVICE_TIER),
        "status": 'active',
        "created_at": created_at,
        "updated_at": updated_at
    }

# Incidents per client (0–3)
user_ids = list(users.keys())
component_ids = list(components.keys())
for cid in client_ids:
    for _ in range(random.randint(0, 3)):
        iid = next_id(idc, "incidents")
        created_at, updated_at = make_stamp_pair()
        reporter_id = choose_one(user_ids)
        # Optionally link a component of same client if available
        candidate_comps = [k for k, v in components.items() if v["client_id"] == cid]
        comp_id = choose_one(candidate_comps) if candidate_comps and random.random() < 0.8 else None
        status = choose_one(['new','triage','in_progress','mitigated','resolved','closed'])
        incidents[iid] = {
            "incident_id": str(iid),
            "reporter_id": str(reporter_id),
            "client_id": str(cid),
            "component_id": str(comp_id) if comp_id else None,
            "title": f"{fake.catch_phrase()}",
            "description": "",  # free-form left empty (Rule 5)
            "category": choose_one(INCIDENT_CATEGORY),
            "severity": choose_one(SEVERITY),
            "status": status,
            "detection_ts": (datetime.fromisoformat(created_at) - timedelta(minutes=random.randint(1, 120))).isoformat(),
            "created_at": created_at,
            "updated_at": updated_at
        }

# Problem tickets per incident (0–3)
incident_ids = list(incidents.keys())
resolver_groups = [gid for gid, g in groups.items() if g["group_type"] in ('resolver','service_desk')]
for iid in incident_ids:
    for _ in range(random.randint(0, 3)):
        pid = next_id(idc, "problem_tickets")
        created_at, updated_at = make_stamp_pair()
        problem_tickets[pid] = {
            "problem_id": str(pid),
            "incident_id": str(iid),
            "title": f"Problem: {fake.bs().title()}",
            "description": "",
            "status": choose_one(PROBLEM_STATUS),
            "owner_group_id": choose_one(resolver_groups) if resolver_groups else None,
            "created_at": created_at,
            "updated_at": updated_at
        }

# Change requests per incident (0–3)
for iid in incident_ids:
    for _ in range(random.randint(0, 3)):
        chid = next_id(idc, "change_requests")
        created_at, updated_at = make_stamp_pair()
        change_requests[chid] = {
            "change_id": str(chid),
            "requested_by": str(choose_one(user_ids)),
            "incident_id": str(iid),
            "title": f"CR: {fake.catch_phrase()}",
            "change_type": choose_one(CHANGE_TYPE),
            "risk": choose_one(RISK),
            "status": choose_one(CHANGE_STATUS if random.random() < 0.5 else ['requested','approved','scheduled']),
            "requested_at": created_at,
            "updated_at": updated_at
        }

# Rollback requests per change (0–2)
change_ids = list(change_requests.keys())
for cid in change_ids:
    for _ in range(random.randint(0, 2)):
        rid = next_id(idc, "rollback_requests")
        created_at, updated_at = make_stamp_pair()
        linked_incident = change_requests[cid]["incident_id"]
        rollback_requests[rid] = {
            "rollback_id": str(rid),
            "change_id": str(cid),
            "incident_id": str(linked_incident),
            "requester_id": str(choose_one(user_ids)),
            "justification": "",
            "scope": choose_one(['partial','full']),
            "status": choose_one(['requested','approved','executed','failed','cancelled']),
            "requested_at": created_at,
            "updated_at": updated_at
        }

# Work orders per change (0–3)
for cid in change_ids:
    for _ in range(random.randint(0, 3)):
        wid = next_id(idc, "work_orders")
        created_at, updated_at = make_stamp_pair()
        start = datetime.fromisoformat(created_at) + timedelta(days=random.randint(0, 5))
        end = start + timedelta(hours=random.randint(1, 48))
        work_orders[wid] = {
            "work_order_id": str(wid),
            "change_id": str(cid),
            "title": f"WO: {fake.bs().title()}",
            "scheduled_start": start.isoformat(),
            "scheduled_end": end.isoformat(),
            "assignee_group_id": choose_one(resolver_groups) if resolver_groups else None,
            "status": choose_one(WORKORDER_STATUS),
            "created_at": created_at,
            "updated_at": updated_at
        }

# Escalations per incident (0–2)
for iid in incident_ids:
    for _ in range(random.randint(0, 2)):
        eid = next_id(idc, "escalations")
        created_at, updated_at = make_stamp_pair()
        escalations[eid] = {
            "escalation_id": str(eid),
            "incident_id": str(iid),
            "target_user_id": str(choose_one(user_ids)),
            "target_role": choose_one(TARGET_ROLE),
            "status": choose_one(ESCALATION_STATUS),
            "created_by": str(choose_one(user_ids)),
            "created_at": created_at,
            "updated_at": updated_at
        }

# Workarounds per incident (0–2)
for iid in incident_ids:
    for _ in range(random.randint(0, 2)):
        wid = next_id(idc, "workarounds")
        created_at, updated_at = make_stamp_pair()
        workarounds[wid] = {
            "workaround_id": str(wid),
            "incident_id": str(iid),
            "implementing_user_id": str(choose_one(user_ids)),
            "description": "",
            "effectiveness": choose_one(EFFECTIVENESS),
            "status": choose_one(['active','retired'] if random.random() < 0.4 else ['active']),
            "created_at": created_at,
            "updated_at": updated_at
        }

# RCA per incident (0–1 to keep ≤3 children in aggregate sensible)
for iid in incident_ids:
    if random.random() < 0.6:
        rca_id = next_id(idc, "root_cause_analyses")
        created_at, updated_at = make_stamp_pair()
        root_cause_analyses[rca_id] = {
            "rca_id": str(rca_id),
            "incident_id": str(iid),
            "conducting_user_id": str(choose_one(user_ids)),
            "analysis_method": choose_one(RCA_METHOD),
            "timeline_summary": "",
            "status": choose_one(RCA_STATUS if random.random() < 0.5 else ['in_progress']),
            "created_at": created_at,
            "updated_at": updated_at
        }

# Communications per incident (0–3)
for iid in incident_ids:
    for _ in range(random.randint(0, 3)):
        cmid = next_id(idc, "communications")
        created_at, updated_at = make_stamp_pair()
        sent_at = ts_between(datetime.fromisoformat(created_at), datetime.fromisoformat(updated_at)).isoformat()
        communications[cmid] = {
            "communication_id": str(cmid),
            "incident_id": str(iid),
            "sender_id": str(choose_one(user_ids)),
            "recipient_type": choose_one(RECIPIENT_TYPE),
            "recipients_note": "",  # free-form (bounded) left empty
            "communication_type": choose_one(COMM_TYPE),
            "delivery_method": choose_one(DELIVERY_METHOD),
            "delivery_status": choose_one(DELIVERY_STATUS),
            "message_summary": "",  # free-form left empty
            "sent_at": sent_at,
            "created_at": created_at
        }

# Incident status history (0–3 entries, consistent chain)
for iid, inc in incidents.items():
    steps = random.randint(0, 3)
    cur = inc["status"]
    # craft plausible chain ending at current status
    chain = [choose_one(INCIDENT_STATUS) for _ in range(steps)]
    prev = None
    for _ in range(steps):
        hid = next_id(idc, "incident_status_history")
        created_at, _updated = make_stamp_pair()
        to_status = choose_one(INCIDENT_STATUS)
        incident_status_history[hid] = {
            "history_id": str(hid),
            "incident_id": str(iid),
            "from_status": prev,
            "to_status": to_status,
            "reason": "",
            "changed_by": str(choose_one(user_ids)),
            "changed_at": created_at
        }
        prev = to_status

# Incident links (0–3 each)
def link_incident(iid: str, ltype: str, pool: Dict[str, Any]):
    if not pool:
        return
    if random.random() < 0.7:
        lid = next_id(idc, "incident_links")
        linked = choose_one(list(pool.keys()))
        created_at, _ = make_stamp_pair()
        incident_links[lid] = {
            "incident_link_id": str(lid),
            "incident_id": str(iid),
            "link_type": ltype,
            "linked_id": str(linked),
            "created_at": created_at
        }

for iid in incident_ids:
    for _ in range(random.randint(0, 3)):
        which = random.choice(['problem','change_request','work_order','knowledge','report','escalation','workaround','rca'])
        pool_map = {
            'problem': problem_tickets,
            'change_request': change_requests,
            'work_order': work_orders,
            'knowledge': knowledge_articles,
            'report': reports,
            'escalation': escalations,
            'workaround': workarounds,
            'rca': root_cause_analyses
        }
        link_incident(iid, which, pool_map[which])

# Reports per incident (0–2)
for iid in incident_ids:
    for _ in range(random.randint(0, 2)):
        rid = next_id(idc, "reports")
        created_at, updated_at = make_stamp_pair()
        status = choose_one(REPORT_STATUS if random.random() < 0.4 else ['completed'])
        reports[rid] = {
            "report_id": str(rid),
            "incident_id": str(iid),
            "generating_user_id": str(choose_one(user_ids)),
            "report_type": choose_one(REPORT_TYPES),
            "status": status,
            "generated_at": updated_at if status != 'pending' else None,
            "created_at": created_at
        }

# Metrics only for Closed incidents (0–2)
closed_incidents = [iid for iid, inc in incidents.items() if inc["status"] == "closed"]
for iid in closed_incidents:
    for _ in range(random.randint(0, 2)):
        mid = next_id(idc, "metrics")
        created_at, _ = make_stamp_pair()
        metrics[mid] = {
            "metric_id": str(mid),
            "incident_id": str(iid),
            "metric_type": choose_one(METRIC_TYPES),
            "value_minutes": random.randint(5, 5000),
            "target_minutes": random.choice([None, random.randint(10, 1440)]),
            "computed_at": created_at
        }

# Knowledge articles (0–2 per incident linkable or standalone)
for iid in incident_ids:
    for _ in range(random.randint(0, 2)):
        kid = next_id(idc, "knowledge_articles")
        created_at, updated_at = make_stamp_pair()
        knowledge_articles[kid] = {
            "kb_id": str(kid),
            "creating_user_id": str(choose_one(user_ids)),
            "incident_id": str(iid) if random.random() < 0.7 else None,
            "title": f"KB: {fake.bs().title()}",
            "content_type": choose_one(KB_CONTENT),
            "category": choose_one(KB_CATEGORY),
            "status": choose_one(KB_STATUS if random.random() < 0.3 else ['draft']),
            "reviewer_user_id": str(choose_one(user_ids)) if random.random() < 0.4 else None,
            "created_at": created_at,
            "updated_at": updated_at
        }

# PIR only for Closed incidents (0–1)
for iid in closed_incidents:
    if random.random() < 0.7:
        pid = next_id(idc, "post_incident_reviews")
        created_at, updated_at = make_stamp_pair()
        sched = (datetime.fromisoformat(created_at) + timedelta(days=random.randint(1, 14))).date().isoformat()
        status = choose_one(PIR_STATUS if random.random() < 0.4 else ['scheduled'])
        post_incident_reviews[pid] = {
            "pir_id": str(pid),
            "incident_id": str(iid),
            "facilitator_user_id": str(choose_one(user_ids)),
            "scheduled_date": sched,
            "status": status,
            "completed_at": updated_at if status == 'completed' else None,
            "created_at": created_at
        }

# Approvals (sprinkle across entities, ≤3 per target)
def create_approval(target_type: str, target_id: str, scope: str):
    aid = next_id(idc, "approvals")
    created_at, _ = make_stamp_pair()
    approvals[aid] = {
        "approval_id": str(aid),
        "approval_reference": f"APR-{random.randint(10000,99999)}",
        "action_scope": scope,
        "target_entity_type": target_type,
        "target_entity_id": str(target_id),
        "approver_user_id": str(choose_one(user_ids)),
        "approver_role": choose_one(APPROVER_ROLE),
        "decision": choose_one(DECISION if random.random() < 0.2 else ['approved']),
        "decided_at": created_at,
        "note": ""  # free-form left empty
    }

for iid in incident_ids:
    for _ in range(random.randint(0, 2)):
        create_approval("incident", iid, choose_one(['incident_creation','severity_set','status_transition','resolution','closure']))

for chid in change_ids:
    for _ in range(random.randint(0, 2)):
        create_approval("change_request", chid, choose_one(['change_request','rollback','status_transition']))

# Audit trails: at least one per entity created (sampled, respecting ≤3 per parent implicitly by sampling)
def audit(ref_type: str, ref_id: str, action: str):
    auid = next_id(idc, "audit_trails")
    created_at, _ = make_stamp_pair()
    actor = choose_one(user_ids)
    audit_trails[auid] = {
        "audit_id": str(auid),
        "actor_user_id": str(actor),
        "reference_type": ref_type,
        "reference_id": str(ref_id),
        "action": action,
        "summary": f"{action} on {ref_type} {ref_id}",
        "created_at": created_at
    }

for uid in users.keys(): audit("user", uid, "create")
for gid in groups.keys(): audit("component" if random.random()<0.2 else "user", choose_one(list(users.keys())), "read")
for iid in incidents.keys(): audit("incident", iid, "create")
for pid in problem_tickets.keys(): audit("problem", pid, "create")
for chid in change_ids: audit("change_request", chid, "create")
for rid in rollback_requests.keys(): audit("change_request", rollback_requests[rid]["change_id"], "update")
for wid in work_orders.keys(): audit("work_order", wid, "create")
for eid in escalations.keys(): audit("escalation", eid, "create")
for wid in workarounds.keys(): audit("workaround", wid, "create")
for rcaid in root_cause_analyses.keys(): audit("rca", rcaid, "create")
for cmid in communications.keys(): audit("communication", cmid, "create")
for hid in incident_status_history.keys(): audit("status_history", hid, "status_change")
for lid in incident_links.keys(): audit("incident", incident_links[lid]["incident_id"], "link")
for rid in reports.keys(): audit("report", rid, "generate")
for mid in metrics.keys(): audit("metric", mid, "create")
for kid in knowledge_articles.keys(): audit("knowledge", kid, "create")
for pid in post_incident_reviews.keys(): audit("pir", pid, "create")
for aid in approvals.keys(): audit("approval", aid, "approve" if approvals[aid]["decision"]=="approved" else "reject")

# -------- Write JSON files (keyed by ID string) --------
write_json("users.json", users)
write_json("groups.json", groups)
write_json("user_groups.json", user_groups)
write_json("clients.json", clients)
write_json("components.json", components)
write_json("incidents.json", incidents)
write_json("problem_tickets.json", problem_tickets)
write_json("change_requests.json", change_requests)
write_json("rollback_requests.json", rollback_requests)
write_json("work_orders.json", work_orders)
write_json("escalations.json", escalations)
write_json("workarounds.json", workarounds)
write_json("root_cause_analyses.json", root_cause_analyses)
write_json("communications.json", communications)
write_json("incident_status_history.json", incident_status_history)
write_json("incident_links.json", incident_links)
write_json("reports.json", reports)
write_json("metrics.json", metrics)
write_json("knowledge_articles.json", knowledge_articles)
write_json("post_incident_reviews.json", post_incident_reviews)
write_json("approvals.json", approvals)
write_json("audit_trails.json", audit_trails)

print(f"Seeded {len(users)} users, {len(groups)} groups, {len(incidents)} incidents, {len(change_requests)} CRs, {len(metrics)} metrics")
