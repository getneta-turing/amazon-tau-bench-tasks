from .assign_incident_priority import AssignIncidentPriority
from .capture_diagnosis_workaround import CaptureDiagnosisWorkaround
from .capture_incident_details import CaptureIncidentDetails
from .create_incident_communication import CreateIncidentCommunication
from .finalize_incident_resolution import FinalizeIncidentResolution
from .find_entities import FindEntities
from .fix_problem import FixProblem
from .get_incident_communications import GetIncidentCommunications
from .initiate_problem import InitiateProblem
from .label_incident import LabelIncident
from .open_postmortem import OpenPostMortem
from .open_vendor_case import OpenVendorCase
from .raise_incident_from_event import RaiseIncidentFromEvent
from .read_incident import ReadIncident
from .read_problem import ReadProblem
from .record_incident_drill import RecordIncidentDrill
from .record_incident_kb_update import RecordIncidentKBUpdate
from .record_tool_activity import RecordToolActivity
from .register_incident import RegisterIncident
from .register_problem_workaround import RegisterProblemWorkaround
from .relate_change_to_incident import RelateChangeToIncident
from .relate_incident_to_problem import RelateIncidentToProblem
from .revise_problem import ReviseProblem
from .route_incident import RouteIncident
from .search_incidents import SearchIncidents
from .terminate_incident import TerminateIncident
from .terminate_problem import TerminateProblem
from .upgrade_incident import upgradeIncident
from .write_audit_record import WriteAuditRecord

ALL_TOOLS_INTERFACE_4 = [
    AssignIncidentPriority,
    CaptureDiagnosisWorkaround,
    CaptureIncidentDetails,
    CreateIncidentCommunication,
    FinalizeIncidentResolution,
    FindEntities,
    FixProblem,
    GetIncidentCommunications,
    InitiateProblem,
    LabelIncident,
    OpenPostMortem,
    OpenVendorCase,
    RaiseIncidentFromEvent,
    ReadIncident,
    ReadProblem,
    RecordIncidentDrill,
    RecordIncidentKBUpdate,
    RecordToolActivity,
    RegisterIncident,
    RegisterProblemWorkaround,
    RelateChangeToIncident,
    RelateIncidentToProblem,
    ReviseProblem,
    RouteIncident,
    SearchIncidents,
    TerminateIncident,
    TerminateProblem,
    upgradeIncident,
    WriteAuditRecord,
]
