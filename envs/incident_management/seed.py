# incident_management/seed.py
import os, json, random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
fake.seed(42)

# ---------------- Time utilities (no Faker relative strings) ----------------
NOW = datetime.utcnow()

def rand_dt_between(start_dt: datetime, end_dt: datetime) -> datetime:
    """Return a random datetime between two datetimes (inclusive of start)."""
    if end_dt < start_dt:
        start_dt, end_dt = end_dt, start_dt
    delta = end_dt - start_dt
    seconds = int(delta.total_seconds())
    return start_dt + timedelta(seconds=random.randint(0, max(seconds, 1)))

def parse_when(expr, base: datetime | None = None) -> datetime:
    """
    Parse a datetime expression:
      - datetime -> returned
      - ISO string -> parsed
      - 'now' -> NOW (or base)
      - '+Nd', '-Nd', '+Nh', '-Nh', '+Nm', '-Nm', '+Ns', '-Ns'
    """
    base = base or NOW
    if isinstance(expr, datetime):
        return expr
    if isinstance(expr, str):
        # try ISO first
        try:
            return datetime.fromisoformat(expr)
        except Exception:
            pass
        e = expr.strip().lower()
        if e == "now":
            return base
        if e and (e[0] in "+-") and e[-1] in "smhdw":
            sign = 1 if e[0] == "+" else -1
            amount = int(e[1:-1])
            unit = e[-1]
            mult = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days", "w": "weeks"}[unit]
            return base + sign * timedelta(**{mult: amount})
    raise ValueError(f"Unsupported datetime expression: {expr!r}")

def iso_between(start_expr, end_expr):
    """Return ISO string between two expressions (datetime or parsable string)."""
    start_dt = parse_when(start_expr)
    end_dt = parse_when(end_expr, base=start_dt)
    return rand_dt_between(start_dt, end_dt).isoformat()

def ts_pair():
    """created_at in [NOW-2y, NOW-30d], updated_at in [created_at, created_at+5d]."""
    start = NOW - timedelta(days=730)
    end = NOW - timedelta(days=30)
    created = rand_dt_between(start, end)
    updated = rand_dt_between(created, created + timedelta(days=5))
    return created.isoformat(), updated.isoformat()

def ts_window(min_days=0, max_days=7, start: datetime | None = None):
    """Return (start_iso, end_iso) within a small window."""
    if start is None:
        start = rand_dt_between(NOW - timedelta(days=180), NOW - timedelta(days=2))
    end = rand_dt_between(start + timedelta(days=min_days), start + timedelta(days=max_days, seconds=86400))
    return start.isoformat(), end.isoformat()

# ---------------- ID generator ----------------
class IdGen:
    def __init__(self):
        self.counters = {}
    def next(self, table_name):
        self.counters.setdefault(table_name, 0)
        self.counters[table_name] += 1
        return str(self.counters[table_name])

ID = IdGen()

def choice_or_none(seq, p_none=0.25):
    return None if random.random() < p_none else random.choice(seq)

# ---------------- Volumes ----------------
TARGET_COUNTS = {
    "users": 14,
    "services": 8,
    "monitoring_events": 10,
    "incidents": 18,
    "incident_assignments": 18,
    "incident_history": 36,
    "incident_workarounds": 7,
    "communications": 24,
    "vendor_engagements": 6,
    "change_requests": 8,
    "approvals": 10,
    "problems": 8,
    "problem_incident_links": 12,
    "problem_workarounds": 5,
    "problem_change_links": 6,
    "knowledge_base_articles": 8,
    "kb_links": 12,
    "tool_usages": 22,
    "simulations": 5,
    "post_incident_reviews": 6,
    "documents": 10,
    "audit_trails": 60
}

# ---------------- Enums ----------------
ROLES = [
    'incident_manager','service_desk_manager','service_desk_analyst',
    'l1','l2','l3','facilities_manager','change_management','developer','end_user'
]
USER_STATUSES = ['active','inactive','suspended']
SERVICE_CRIT = ['low','medium','high']
SERVICE_STATUS = ['active','inactive']
DETECTION = ['user_report','monitoring_tool','automated_alert']
CATEGORIES = ['hardware','software','security','performance','other']
PRIORITIES = ['low','medium','high']
SEVERITIES = ['low','medium','high']
INC_STATUS = ['open','in_progress','escalated','pending_vendor','resolved','closed']
ASSIGN_TEAMS = ['service_desk','l1','l2','l3','facilities','change_mgmt','devops','incident_manager']
RECIPIENTS = ['end_users','stakeholders','executives','IT_staff']
VENDOR_METHOD = ['phone','email','vendor_portal','API']
VENDOR_STATUS = ['initiated','pending_vendor','vendor_responded','closed']
APPROVAL_REF_TYPES = ['incident','change','problem','kb','vendor']
APPROVAL_TYPES = ['authorization','closure','change']
APPROVAL_STATUS = ['pending','approved','rejected']
PROB_STATUS = ['open','under_investigation','workaround_available','resolved','closed']
KB_STATUS = ['draft','published','archived']
TOOL_TYPES = ['monitoring','root_cause_analysis','ITSM_service_desk','incident_response','AI_virtual_agent','AIOps','automation_script']
TOOL_OUTCOME = ['noted','applied','recommended']
DOC_FORMAT = ['pdf','xlsx','docx','csv','txt','png','jpg','other']
DOC_CONF = ['public','internal','confidential','restricted']
DOC_STATUS = ['available','archived','deleted']
AUD_REF_TYPES = ['incident','communication','review','kb','tool_use','vendor','problem','change','simulation','monitoring_event','assignment','document']
AUD_ACTIONS = ['identify','create','read','update','approve','reject','close','notify','escalate','resolve','review','kb_update','vendor_engagement','simulation','tool_use','link']

# ---------------- Tables (as dicts) ----------------
users = {}
services = {}
monitoring_events = {}
incidents = {}
incident_assignments = {}
incident_history = {}
incident_workarounds = {}
communications = {}
vendor_engagements = {}
change_requests = {}
approvals = {}
problems = {}
problem_incident_links = {}
problem_workarounds = {}
problem_change_links = {}
knowledge_base_articles = {}
kb_links = {}
tool_usages = {}
simulations = {}
post_incident_reviews = {}
documents = {}
audit_trails = {}

# ---------------- Data generation ----------------
domains = ["example.com","contoso.com","fabrikam.io","acme.org","mailhub.net"]
role_quota = {
    'incident_manager': 1, 'service_desk_manager': 1, 'service_desk_analyst': 3,
    'l1': 2, 'l2': 2, 'l3': 2, 'facilities_manager': 1, 'change_management': 1,
    'developer': 1, 'end_user': 0
}
role_list = []
for r, q in role_quota.items():
    role_list += [r]*q
while len(role_list) < TARGET_COUNTS["users"]:
    role_list.append('end_user')
random.shuffle(role_list)

# Users
for _ in range(TARGET_COUNTS["users"]):
    user_id = ID.next("users")
    full_name = fake.name()
    fn = full_name.split()[0].lower()
    ln = full_name.split()[-1].lower()
    email = f"{fn}.{ln}{random.randint(1,9999)}@{random.choice(domains)}"
    tz = fake.timezone()
    created_at, updated_at = ts_pair()
    role = role_list.pop() if role_list else random.choice(ROLES)
    users[user_id] = {
        "user_id": str(user_id),
        "full_name": full_name,
        "email": email,
        "role": role,
        "timezone": tz,
        "status": random.choice(USER_STATUSES if role != 'incident_manager' else ['active']),
        "created_at": created_at,
        "updated_at": updated_at
    }

# Services (≤3 per owner)
owner_ids = [uid for uid, u in users.items() if u["role"] in ("service_desk_manager","incident_manager","l2","l3","developer")]
owner_service_counts = {uid: 0 for uid in owner_ids}
for _ in range(TARGET_COUNTS["services"]):
    owner = random.choice(owner_ids)
    if owner_service_counts[owner] >= 3:
        owners_left = [o for o in owner_ids if owner_service_counts[o] < 3]
        owner = random.choice(owners_left) if owners_left else owner
    service_id = ID.next("services")
    name = f"{fake.bs().title()} Service"
    created_at, updated_at = ts_pair()
    services[service_id] = {
        "service_id": str(service_id),
        "name": name,
        "owner_user_id": str(owner),
        "criticality": random.choice(SERVICE_CRIT),
        "status": random.choice(SERVICE_STATUS),
        "created_at": created_at,
        "updated_at": updated_at
    }
    owner_service_counts[owner] += 1

# Monitoring events (≤2 per service)
svc_ids = list(services.keys())
svc_event_counts = {sid: 0 for sid in svc_ids}
for _ in range(TARGET_COUNTS["monitoring_events"]):
    if not svc_ids: break
    svc = random.choice(svc_ids)
    if svc_event_counts[svc] >= 2:
        candidates = [s for s in svc_ids if svc_event_counts[s] < 2]
        if candidates:
            svc = random.choice(candidates)
    event_id = ID.next("monitoring_events")
    occurred, ingested = ts_window()
    monitoring_events[event_id] = {
        "event_id": str(event_id),
        "detected_service_id": str(svc),
        "source": random.choice(['monitoring_tool','automated_alert']),
        "alert_type": random.choice(["CPUHigh","MemoryPressure","DiskFull","ServiceDown","AuthErrors"]),
        "severity": random.choice(SEVERITIES),
        "occurred_at": occurred,
        "ingested_at": ingested,
        "created_by_user_id": choice_or_none(list(users.keys()), p_none=0.4)
    }
    svc_event_counts[svc] += 1

# Incidents (≤3 per reporter)
reporters = list(users.keys())
reporter_counts = {r: 0 for r in reporters}
high_incident_ids = []
for _ in range(TARGET_COUNTS["incidents"]):
    rep = random.choice(reporters)
    if reporter_counts[rep] >= 3:
        pool = [r for r in reporters if reporter_counts[r] < 3]
        rep = random.choice(pool) if pool else rep
    inc_id = ID.next("incidents")
    created_at, _ = ts_pair()
    src_ev = choice_or_none(list(monitoring_events.keys()), p_none=0.5)
    aff_svc = choice_or_none(svc_ids, p_none=0.2)
    priority = random.choices(PRIORITIES, weights=[0.45,0.4,0.15])[0]
    status = random.choices(INC_STATUS, weights=[0.4,0.25,0.1,0.05,0.15,0.05])[0]
    resolved_at = closed_at = resolved_by = closed_by = None
    if status in ("resolved","closed"):
        resolved_at = iso_between(created_at, "+2d")
        resolved_by = choice_or_none(list(users.keys()), p_none=0.0)
        if status == "closed":
            closed_at = iso_between(resolved_at, "+3d")
            closed_by = choice_or_none(list(users.keys()), p_none=0.0)
    incidents[inc_id] = {
        "incident_id": str(inc_id),
        "reporter_id": str(rep),
        "detection_source": random.choice(DETECTION),
        "category": random.choice(CATEGORIES),
        "priority": priority,
        "severity": random.choice(SEVERITIES),
        "status": status,
        "affected_service_id": aff_svc,
        "initial_description": "",
        "source_event_id": src_ev,
        "created_at": created_at,
        "resolved_at": resolved_at,
        "closed_at": closed_at,
        "resolved_by_user_id": resolved_by,
        "closed_by_user_id": closed_by
    }
    if priority == "high":
        high_incident_ids.append(inc_id)
    reporter_counts[rep] += 1

# Incident assignments (1 per incident)
for inc_id in incidents.keys():
    assigned_team = random.choice(ASSIGN_TEAMS)
    responder = choice_or_none([uid for uid, u in users.items() if u["role"] in ("service_desk_analyst","l1","l2","l3","incident_manager")], p_none=0.2)
    assign_id = ID.next("incident_assignments")
    assigned_at, _ = ts_pair()
    incident_assignments[assign_id] = {
        "assignment_id": str(assign_id),
        "incident_id": str(inc_id),
        "assigned_team": assigned_team,
        "responder_user_id": responder,
        "assigned_at": assigned_at,
        "unassigned_at": None
    }

# Incident history (≤2 per incident)
for inc_id, inc in incidents.items():
    n = random.randint(0, 2)
    for _ in range(n):
        h_id = ID.next("incident_history")
        field = random.choice(['status','priority','severity','category','assignment','workaround'])
        old_v = str(inc.get(field, random.choice(PRIORITIES)))
        new_v = random.choice({
            'status': INC_STATUS,
            'priority': PRIORITIES,
            'severity': SEVERITIES,
            'category': CATEGORIES,
            'assignment': ASSIGN_TEAMS,
            'workaround': ['added','updated','removed']
        }[field])
        changed_at, _ = ts_pair()
        changer = random.choice(list(users.keys()))
        incident_history[h_id] = {
            "history_id": str(h_id),
            "incident_id": str(inc_id),
            "changed_by_user_id": str(changer),
            "field": field,
            "old_value": old_v,
            "new_value": str(new_v),
            "changed_at": changed_at
        }

# Incident workarounds (0–1 per some)
candidate_incidents = random.sample(list(incidents.keys()), k=min(TARGET_COUNTS["incident_workarounds"], len(incidents)))
for inc_id in candidate_incidents:
    iw_id = ID.next("incident_workarounds")
    applied_by = random.choice(list(users.keys()))
    applied_at, _ = ts_pair()
    incident_workarounds[iw_id] = {
        "incident_workaround_id": str(iw_id),
        "incident_id": str(inc_id),
        "summary": "",
        "applied_by_user_id": str(applied_by),
        "applied_at": applied_at,
        "active": random.choice([True, False])
    }

# Communications (0–3 per incident)
for inc_id in incidents.keys():
    n = random.randint(0, 3)
    for _ in range(n):
        c_id = ID.next("communications")
        created_at, _ = ts_pair()
        sent_by = random.choice(list(users.keys()))
        communications[c_id] = {
            "communication_id": str(c_id),
            "incident_id": str(inc_id),
            "recipients": random.choice(RECIPIENTS),
            "message_text": "",
            "sent_by_user_id": str(sent_by),
            "created_at": created_at
        }

# Vendor engagements (subset)
ve_incidents = random.sample(list(incidents.keys()), k=min(TARGET_COUNTS["vendor_engagements"], len(incidents)))
for inc_id in ve_incidents:
    ve_id = ID.next("vendor_engagements")
    created_at, updated_at = ts_pair()
    initiated_by = random.choice(list(users.keys()))
    vendor_engagements[ve_id] = {
        "vendor_engagement_id": str(ve_id),
        "incident_id": str(inc_id),
        "vendor_name": random.choice(["Atlassian","ServiceNow","SolarWinds","BMC","Ivanti","OpenText","ManageEngine","4me","Freshworks","TeamDynamix"]),
        "contact_method": random.choice(VENDOR_METHOD),
        "vendor_ticket_reference": f"V-{random.randint(10000,99999)}",
        "status": random.choice(VENDOR_STATUS),
        "initiated_by_user_id": str(initiated_by),
        "created_at": created_at,
        "updated_at": updated_at
    }

# Change requests (subset)
chg_incidents = random.sample(list(incidents.keys()), k=min(TARGET_COUNTS["change_requests"], len(incidents)))
for inc_id in chg_incidents:
    chg_id = ID.next("change_requests")
    requested_by = random.choice([uid for uid, u in users.items() if u["role"] in ("change_management","l2","l3","developer","incident_manager")])
    created_at, _ = ts_pair()
    approval_status = random.choice(['pending','approved','rejected'])
    approved_by_user_id = None
    approved_at = None
    if approval_status in ('approved','rejected'):
        approved_by_user_id = random.choice([uid for uid, u in users.items() if u["role"] in ("change_management","incident_manager")])
        _, approved_at = ts_pair()
    implemented_at = None
    if approval_status == 'approved' and random.random() < 0.6:
        _, implemented_at = ts_pair()
    change_requests[chg_id] = {
        "change_id": str(chg_id),
        "incident_id": str(inc_id),
        "requested_by_user_id": str(requested_by),
        "summary": "",
        "approval_status": approval_status,
        "approved_by_user_id": approved_by_user_id,
        "approved_at": approved_at,
        "implemented_at": implemented_at,
        "created_at": created_at
    }

# Approvals
ref_buckets = []
ref_buckets += [('incident', iid) for iid in list(incidents.keys())[:4]]
ref_buckets += [('change', cid) for cid in list(change_requests.keys())[:4]]
ref_buckets += [('vendor', vid) for vid in list(vendor_engagements.keys())[:2]]
random.shuffle(ref_buckets)
for i in range(min(TARGET_COUNTS["approvals"], len(ref_buckets))):
    app_id = ID.next("approvals")
    ref_type, ref_id = ref_buckets[i]
    created_at, decided_at = ts_pair()
    approver = random.choice([uid for uid, u in users.items() if u["role"] in ("incident_manager","service_desk_manager","change_management")])
    approvals[app_id] = {
        "approval_id": str(app_id),
        "reference_type": ref_type,
        "reference_id": str(ref_id),
        "approval_type": random.choice(APPROVAL_TYPES),
        "status": random.choice(APPROVAL_STATUS),
        "approved_by_user_id": str(approver),
        "created_at": created_at,
        "decided_at": decided_at,
        "notes": ""
    }

# Problems
for _ in range(TARGET_COUNTS["problems"]):
    pid = ID.next("problems")
    created_at, _ = ts_pair()
    problems[pid] = {
        "problem_id": str(pid),
        "title": fake.catch_phrase(),
        "description": "",
        "detection_source": random.choice(DETECTION),
        "status": random.choice(PROB_STATUS),
        "known_error": random.choice([False, False, True]),
        "created_by_user_id": random.choice(list(users.keys())),
        "resolved_by_user_id": None,
        "closed_by_user_id": None,
        "created_at": created_at,
        "resolved_at": None,
        "closed_at": None
    }

# Problem-incident links (≤3 per problem)
prob_ids = list(problems.keys())
inc_ids = list(incidents.keys())
prob_link_counts = {p: 0 for p in prob_ids}
linked_pairs = set()
for _ in range(TARGET_COUNTS["problem_incident_links"]):
    if not prob_ids or not inc_ids: break
    p = random.choice(prob_ids)
    if prob_link_counts[p] >= 3:
        candidates = [x for x in prob_ids if prob_link_counts[x] < 3]
        if candidates:
            p = random.choice(candidates)
    i = random.choice(inc_ids)
    if (p, i) in linked_pairs:
        continue
    link_id = ID.next("problem_incident_links")
    linked_pairs.add((p, i))
    prob_link_counts[p] += 1
    problem_incident_links[link_id] = {
        "link_id": str(link_id),
        "problem_id": str(p),
        "incident_id": str(i),
        "linked_by_user_id": random.choice(list(users.keys())),
        "linked_at": iso_between(NOW - timedelta(days=60), NOW)
    }

# Problem workarounds (subset)
wk_probs = random.sample(prob_ids, k=min(TARGET_COUNTS["problem_workarounds"], len(prob_ids)))
for p in wk_probs:
    wid = ID.next("problem_workarounds")
    added_at, _ = ts_pair()
    problem_workarounds[wid] = {
        "workaround_id": str(wid),
        "problem_id": str(p),
        "summary": "",
        "added_by_user_id": random.choice(list(users.keys())),
        "added_at": added_at,
        "active": random.choice([True, False])
    }

# Problem-change links (subset)
chg_ids = list(change_requests.keys())
pl_probs = random.sample(prob_ids, k=min(TARGET_COUNTS["problem_change_links"], len(prob_ids)))
for p in pl_probs:
    if not chg_ids:
        break
    cid = random.choice(chg_ids)
    lid = ID.next("problem_change_links")
    problem_change_links[lid] = {
        "link_id": str(lid),
        "problem_id": str(p),
        "change_id": str(cid),
        "linked_by_user_id": random.choice(list(users.keys())),
        "linked_at": iso_between(NOW - timedelta(days=30), NOW)
    }

# KB articles
for _ in range(TARGET_COUNTS["knowledge_base_articles"]):
    kbid = ID.next("knowledge_base_articles")
    created_at, updated_at = ts_pair()
    knowledge_base_articles[kbid] = {
        "kb_id": str(kbid),
        "title": fake.bs().title(),
        "content_summary": "",
        "status": random.choice(KB_STATUS),
        "created_by_user_id": random.choice(list(users.keys())),
        "created_at": created_at,
        "updated_at": updated_at
    }

# KB links
kb_ids = list(knowledge_base_articles.keys())
refs_pool = []
refs_pool += [('incident', iid) for iid in random.sample(inc_ids, k=min(6, len(inc_ids)))]
refs_pool += [('problem', pid) for pid in random.sample(prob_ids, k=min(4, len(prob_ids)))]
refs_pool += [('change', cid) for cid in random.sample(chg_ids, k=min(2, len(chg_ids)))]
random.shuffle(refs_pool)
for i in range(min(TARGET_COUNTS["kb_links"], len(refs_pool))):
    kid = random.choice(kb_ids)
    ref_type, ref_id = refs_pool[i]
    link_id = ID.next("kb_links")
    kb_links[link_id] = {
        "kb_link_id": str(link_id),
        "kb_id": str(kid),
        "reference_type": ref_type,
        "reference_id": str(ref_id),
        "linked_by_user_id": random.choice(list(users.keys())),
        "linked_at": iso_between(NOW - timedelta(days=20), NOW)
    }

# Tool usages (≤2 per incident)
for inc_id in incidents.keys():
    n = random.randint(0, 2)
    for _ in range(n):
        tu_id = ID.next("tool_usages")
        executed_at, _ = ts_pair()
        tool_usages[tu_id] = {
            "tool_usage_id": str(tu_id),
            "incident_id": str(inc_id),
            "tool_used": random.choice(TOOL_TYPES),
            "action_summary": "",
            "executed_by_user_id": random.choice(list(users.keys())),
            "executed_at": executed_at,
            "outcome": random.choice(TOOL_OUTCOME)
        }

# Simulations
for _ in range(TARGET_COUNTS["simulations"]):
    sid = ID.next("simulations")
    started, ended = ts_window()
    simulations[sid] = {
        "simulation_id": str(sid),
        "scenario_name": f"Drill {fake.word().title()}",
        "simulated_by_user_id": random.choice([uid for uid, u in users.items() if u["role"] == "incident_manager"]),
        "scope": random.choice([s["name"] for s in services.values()]) if services else "Core Service",
        "started_at": started,
        "ended_at": ended,
        "outcome": random.choice(['completed','failed']),
        "notes": ""
    }

# Post-incident reviews (for high-priority)
pir_candidates = [iid for iid in set(high_incident_ids) if incidents[iid]["status"] in ("resolved","closed","in_progress","escalated","open")]
random.shuffle(pir_candidates)
for iid in pir_candidates[:TARGET_COUNTS["post_incident_reviews"]]:
    rid = ID.next("post_incident_reviews")
    post_incident_reviews[rid] = {
        "review_id": str(rid),
        "incident_id": str(iid),
        "conducted_by_user_id": random.choice([uid for uid, u in users.items() if u["role"] == "incident_manager"]),
        "notes": "",
        "created_at": iso_between(NOW - timedelta(days=10), NOW)
    }

# Documents
for _ in range(TARGET_COUNTS["documents"]):
    did = ID.next("documents")
    upload, _ = ts_pair()
    inc_ref = prob_ref = chg_ref = None
    attach_choice = random.choice(['incident','problem','change','none','none'])
    if attach_choice == 'incident' and inc_ids:
        inc_ref = random.choice(inc_ids)
    elif attach_choice == 'problem' and prob_ids:
        prob_ref = random.choice(prob_ids)
    elif attach_choice == 'change' and chg_ids:
        chg_ref = random.choice(chg_ids)
    documents[did] = {
        "document_id": str(did),
        "name": f"{fake.file_name(category='text')}",
        "format": random.choice(DOC_FORMAT),
        "uploaded_by_user_id": random.choice(list(users.keys())),
        "upload_date": upload,
        "size_bytes": random.randint(5_000, 2_000_000),
        "confidentiality": random.choice(DOC_CONF),
        "status": random.choice(DOC_STATUS),
        "incident_id": inc_ref,
        "problem_id": prob_ref,
        "change_id": chg_ref
    }

# Audit trails
def add_audit(ref_type, ref_id, action):
    aid = ID.next("audit_trails")
    audit_trails[aid] = {
        "audit_trail_id": str(aid),
        "reference_type": ref_type,
        "reference_id": str(ref_id),
        "action": action,
        "user_id": random.choice(list(users.keys())),
        "field_name": None,
        "old_value": "",
        "new_value": "",
        "created_at": iso_between(NOW - timedelta(days=15), NOW)
    }

for inc_id in list(incidents.keys())[:20]:
    add_audit("incident", inc_id, random.choice(["identify","create","update","resolve","close","notify"]))
for c_id in list(communications.keys())[:12]:
    add_audit("communication", c_id, "notify")
for v_id in list(vendor_engagements.keys())[:6]:
    add_audit("vendor", v_id, "vendor_engagement")
for chg_id in list(change_requests.keys())[:8]:
    add_audit("change", chg_id, random.choice(["create","approve","reject","update"]))
for pr_id in list(problems.keys())[:10]:
    add_audit("problem", pr_id, random.choice(["create","update","link"]))
for kb_id in list(knowledge_base_articles.keys())[:8]:
    add_audit("kb", kb_id, random.choice(["create","kb_update"]))
for tu_id in list(tool_usages.keys())[:10]:
    add_audit("tool_use", tu_id, "tool_use")
for me_id in list(monitoring_events.keys())[:8]:
    add_audit("monitoring_event", me_id, "create")
for a_id in list(incident_assignments.keys())[:10]:
    add_audit("assignment", a_id, "update")
for d_id in list(documents.keys())[:8]:
    add_audit("document", d_id, "create")

# ---------------- Write JSON outputs ----------------
os.makedirs("seed", exist_ok=True)

def dump(name, obj):
    with open(os.path.join("seed", f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in obj.items()}, f, indent=2, ensure_ascii=False)

dump("users", users)
dump("services", services)
dump("monitoring_events", monitoring_events)
dump("incidents", incidents)
dump("incident_assignments", incident_assignments)
dump("incident_history", incident_history)
dump("incident_workarounds", incident_workarounds)
dump("communications", communications)
dump("vendor_engagements", vendor_engagements)
dump("change_requests", change_requests)
dump("approvals", approvals)
dump("problems", problems)
dump("problem_incident_links", problem_incident_links)
dump("problem_workarounds", problem_workarounds)
dump("problem_change_links", problem_change_links)
dump("knowledge_base_articles", knowledge_base_articles)
dump("kb_links", kb_links)
dump("tool_usages", tool_usages)
dump("simulations", simulations)
dump("post_incident_reviews", post_incident_reviews)
dump("documents", documents)
dump("audit_trails", audit_trails)

print("✔ IMS seed data generated in ./seed/*.json")
