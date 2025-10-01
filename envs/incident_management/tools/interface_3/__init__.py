from .advance_incident import AdvanceIncident
from .amend_problem import AmendProblem
from .assign_incident_category import AssignIncidentCategory
from .browse_incidents import BrowseIncidents
from .conclude_incident import ConcludeIncident
from .conclude_problem import ConcludeProblem
from .connect_change_to_incident import ConnectChangeToIncident
from .connect_incident_to_problem import ConnectIncidentToProblem
from .create_incident_from_alert import CreateIncidentFromAlert
from .dispatch_incident import DispatchIncident
from .document_incident_details import DocumentIncidentDetails
from .document_incident_simulation import DocumentIncidentSimulation
from .document_problem_workaround import DocumentProblemWorkaround
from .document_tool_usage import DocumentToolUsage
from .initiate_incident import InitiateIncident
from .log_diagnosis_workaround import LogDiagnosisWorkaround
from .log_incident_communication import LogIncidentCommunication
from .record_audit_entry import RecordAuditEntry
from .rectify_incident import RectifyIncident
from .rectify_problem import RectifyProblem
from .register_problem import RegisterProblem
from .register_vendor_engagement import RegisterVendorEngagement
from .retrieve_incident_communications import RetrieveIncidentCommunications
from .retrieve_incident import RetrieveIncident
from .retrieve_problem import RetrieveProblem
from .search_entities import SearchEntities
from .set_incident_priority import SetIncidentPriority
from .start_post_incident_review import StartPostIncidentReview
from .update_kb_with_incident import UpdateKbWithIncident

ALL_TOOLS_INTERFACE_3 = [
    AdvanceIncident,
    AmendProblem,
    AssignIncidentCategory,
    BrowseIncidents,
    ConcludeIncident,
    ConcludeProblem,
    ConnectChangeToIncident,
    ConnectIncidentToProblem,
    CreateIncidentFromAlert,
    DispatchIncident,
    DocumentIncidentDetails,
    DocumentIncidentSimulation,
    DocumentProblemWorkaround,
    DocumentToolUsage,
    InitiateIncident,
    LogDiagnosisWorkaround,
    LogIncidentCommunication,
    RecordAuditEntry,
    RectifyIncident,
    RectifyProblem,
    RegisterProblem,
    RegisterVendorEngagement,
    RetrieveIncidentCommunications,
    RetrieveIncident,
    RetrieveProblem,
    SearchEntities,
    SetIncidentPriority,
    StartPostIncidentReview,
    UpdateKbWithIncident
]
