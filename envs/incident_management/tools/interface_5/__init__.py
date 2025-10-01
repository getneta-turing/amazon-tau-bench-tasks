from .add_incident_update import AddIncidentUpdate
from .add_problem_workaround import AddProblemWorkaround
from .apply_incident_kb_update import ApplyIncidentKbUpdate
from .attach_change_to_incident import AttachChangeToIncident
from .close_out_incident import CloseOutIncident
from .close_problem import CloseProblem
from .conclude_incident_resolution import ConcludeIncidentResolution
from .create_pir_record import CreatePirRecord
from .create_problem import CreateProblem
from .derive_incident_from_monitoring import DeriveIncidentFromMonitoring
from .designate_incident import DesignateIncident
from .escalate_ticket import EscalateTicket
from .file_incident import FileIncident
from .get_incident_record import GetIncidentRecord
from .get_problem_record import GetProblemRecord
from .grade_incident_priority import GradeIncidentPriority
from .group_incident import GroupIncident
from .link_problem_incident import LinkProblemIncident
from .list_incident_communications import ListIncidentCommunications
from .log_vendor_engagement import LogVendorEngagement
from .note_incident_details import NoteIncidentDetails
from .query_incidents import QueryIncidents
from .record_triage_workaround import RecordTriageWorkaround
from .register_audit_event import RegisterAuditEvent
from .register_incident_simulation import RegisterIncidentSimulation
from .register_tool_usage import RegisterToolUsage
from resolve_problem import ResolveProblem
from .retrieve_entities import RetrieveEntities
from .update_problem import UpdateProblem

ALL_TOOLS_INTERFACE_5 = [
    AddIncidentUpdate,
    AddProblemWorkaround,
    ApplyIncidentKbUpdate,
    AttachChangeToIncident,
    CloseOutIncident,
    CloseProblem,
    ConcludeIncidentResolution,
    CreatePirRecord,
    CreateProblem,
    DeriveIncidentFromMonitoring,
    DesignateIncident,
    EscalateTicket,
    FileIncident,
    GetIncidentRecord,
    GetProblemRecord,
    GradeIncidentPriority,
    GroupIncident,
    LinkProblemIncident,
    ListIncidentCommunications,
    LogVendorEngagement,
    NoteIncidentDetails,
    QueryIncidents,
    RecordTriageWorkaround,
    RegisterAuditEvent,
    RegisterIncidentSimulation,
    RegisterToolUsage,
    ResolveProblem,
    RetrieveEntities,
    UpdateProblem,
]
