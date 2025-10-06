# interface_2/__init__.py
from .find_entities import FindEntities
from .log_event_record import LogEventRecord
from .correlate_events import CorrelateEvents
from .register_client import RegisterClient
from .add_user import AddUser
from .onboard_vendor import OnboardVendor
from .register_product import RegisterProduct
from .register_component import RegisterComponent
from .start_subscription import StartSubscription
from .define_sla import DefineSla
from .open_incident import OpenIncident
from .log_communication import LogCommunication
from .apply_workaround import ApplyWorkaround
from .initiate_rca import InitiateRca
from .raise_escalation import RaiseEscalation
from .submit_change_request import SubmitChangeRequest
from .submit_rollback_request import SubmitRollbackRequest
from .log_metric import LogMetric
from .produce_incident_report import ProduceIncidentReport
from .draft_kb_article import DraftKbArticle
from .schedule_post_incident_review import SchedulePostIncidentReview
from .fetch_incident import FetchIncident
from .fetch_event_records import FetchEventRecords
from .fetch_escalations import FetchEscalations
from .fetch_communications import FetchCommunications
from .fetch_kb_articles import FetchKbArticles
from .modify_client import ModifyClient
from .modify_user_permissions import ModifyUserPermissions
from .modify_product import ModifyProduct
from .modify_component import ModifyComponent
from .modify_subscription import ModifySubscription
from .modify_sla import ModifySla
from .modify_incident import ModifyIncident
from .modify_escalation import ModifyEscalation
from .modify_change_request import ModifyChangeRequest
from .modify_rollback_request import ModifyRollbackRequest
from .modify_rca import ModifyRca
from .modify_communication import ModifyCommunication
from .modify_kb_article import ModifyKbArticle
from .modify_post_incident_review import ModifyPostIncidentReview
from .mark_incident_resolved import MarkIncidentResolved
from .finalize_incident import FinalizeIncident
from .assess_severity import AssessSeverity
from .verify_approval import VerifyApproval
from .write_audit_trail import WriteAuditTrail
from .escalate_to_human import EscalateToHuman

ALL_TOOLS_INTERFACE_2 = [
    FindEntities,
    LogEventRecord,
    CorrelateEvents,
    RegisterClient,
    AddUser,
    OnboardVendor,
    RegisterProduct,
    RegisterComponent,
    StartSubscription,
    DefineSla,
    OpenIncident,
    LogCommunication,
    ApplyWorkaround,
    InitiateRca,
    RaiseEscalation,
    SubmitChangeRequest,
    SubmitRollbackRequest,
    LogMetric,
    ProduceIncidentReport,
    DraftKbArticle,
    SchedulePostIncidentReview,
    FetchIncident,
    FetchEventRecords,
    FetchEscalations,
    FetchCommunications,
    FetchKbArticles,
    ModifyClient,
    ModifyUserPermissions,
    ModifyProduct,
    ModifyComponent,
    ModifySubscription,
    ModifySla,
    ModifyIncident,
    ModifyEscalation,
    ModifyChangeRequest,
    ModifyRollbackRequest,
    ModifyRca,
    ModifyCommunication,
    ModifyKbArticle,
    ModifyPostIncidentReview,
    MarkIncidentResolved,
    FinalizeIncident,
    AssessSeverity,
    VerifyApproval,
    WriteAuditTrail,
    EscalateToHuman,
]
