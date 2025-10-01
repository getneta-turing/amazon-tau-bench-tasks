from .create_incident import CreateIncident
from .add_incident_communication import AddIncidentCommunication
from .assign_incident import AssignIncident
from .audit_log_action import AuditLogAction
from .categorize_incident import CategorizeIncident
from .close_incident import CloseIncident
from .create_incident_from_monitoring_event import CreateIncidentFromMonitoringEvent
from .create_post_incident_review import CreatePostIncidentReview
from .create_vendor_engagement import CreateVendorEngagement
from .entities_lookup import EntitiesLookup
from .escalate_incident import EscalateIncident
from .get_incident import GetIncident
from .get_problem import GetProblem
from .link_change_to_incident import LinkChangeToIncident
from .list_communications import ListCommunications
from .list_incidents import ListIncidents
from .log_incident_details import LogIncidentDetails
from .prioritize_incident import PrioritizeIncident
from .problem_add_workaround import ProblemAddWorkaround
from .problem_close import ProblemClose
from .problem_create import ProblemCreate
from .problem_link_incident import ProblemLinkIncident
from .problem_resolve import ProblemResolve
from .problem_update import ProblemUpdate
from .record_diagnosis_workaround import RecordDiagnosisWorkaround
from .record_incident_simulation import RecordIncidentSimulation
from .record_tool_usage import RecordToolUsage
from .update_knowledge_base_from_incident import UpdateKnowledgeBaseFromIncident

ALL_TOOLS_INTERFACE_1 = [
    CreateIncident,
    AddIncidentCommunication,
    AssignIncident,
    AuditLogAction,
    CategorizeIncident,
    CloseIncident,
    CreateIncidentFromMonitoringEvent,
    CreatePostIncidentReview,
    CreateVendorEngagement,
    EntitiesLookup,
    EscalateIncident,
    GetIncident,
    GetProblem,
    LinkChangeToIncident,
    ListCommunications,
    ListIncidents,
    LogIncidentDetails,
    PrioritizeIncident,
    ProblemAddWorkaround,
    ProblemClose,
    ProblemCreate,
    ProblemLinkIncident,
    ProblemResolve,
    ProblemUpdate,
    RecordDiagnosisWorkaround,
    RecordIncidentSimulation,
    RecordToolUsage,
    UpdateKnowledgeBaseFromIncident
]
