from .allocate_incident import AllocateIncident
from .associate_change_with_incident import AssociateChangeWithIncident
from .associate_incident_with_problem import AssociateIncidentWithProblem
from .classify_incident import ClassifyIncident
from .document_diagnosis_workaround import DocumentDiagnosisWorkaround
from .elevate_incident import ElevateIncident
from .enumerate_incidents import EnumerateIncidents
from .fetch_incident import FetchIncident
from .fetch_incident_communications import FetchIncidentCommunications
from .fetch_problem import FetchProblem
from .finalize_incident import FinalizeIncident
from .finalize_problem import FinalizeProblem
from .generate_incident_from_event import GenerateIncidentFromEvent
from .initiate_post_incident_review import InitiatePostIncidentReview
from .initiate_vendor_engagement import InitiateVendorEngagement
from .log_audit_action import LogAuditAction
from .log_incident_simulation import LogIncidentSimulation
from .log_tool_usage import LogToolUsage
from .modify_problem import ModifyProblem
from .open_incident import OpenIncident
from .open_problem import OpenProblem
from .publish_incident_kb_update import PublishIncidentKbUpdate
from .query_entities import QueryEntities
from .rank_incident import RankIncident
from .record_incident_communication import RecordIncidentCommunication
from .record_incident_details import RecordIncidentDetails
from .record_problem_workaround import RecordProblemWorkaround
from .remedy_incident import RemedyIncident
from .remedy_problem import RemedyProblem

ALL_TOOLS_INTERFACE_2 = [
    OpenIncident,
    AllocateIncident,
    AssociateChangeWithIncident,
    AssociateIncidentWithProblem,
    ClassifyIncident,
    DocumentDiagnosisWorkaround,
    ElevateIncident,
    EnumerateIncidents,
    FetchIncident,
    FetchIncidentCommunications,
    FetchProblem,
    FinalizeIncident,
    FinalizeProblem,
    GenerateIncidentFromEvent,
    InitiatePostIncidentReview,
    InitiateVendorEngagement,
    LogAuditAction,
    LogIncidentSimulation,
    LogToolUsage,
    ModifyProblem,
    OpenProblem,
    PublishIncidentKbUpdate,
    QueryEntities,
    RankIncident,
    RecordIncidentCommunication,
    RecordIncidentDetails,
    RecordProblemWorkaround,
    RemedyIncident,
    RemedyProblem,
]
