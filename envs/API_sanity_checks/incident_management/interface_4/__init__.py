# interface_4/__init__.py
from .identify_entities import IdentifyEntities
from .record_event_entry import RecordEventEntry
from .associate_events_once import AssociateEventsOnce
from .register_customer import RegisterCustomer
from .register_user import RegisterUser
from .onboard_supplier import OnboardSupplier
from .add_product_record import AddProductRecord
from .add_component_record import AddComponentRecord
from .provision_subscription import ProvisionSubscription
from .specify_sla import SpecifySla
from .log_incident import LogIncident
from .record_communication_entry import RecordCommunicationEntry
from .enact_workaround import EnactWorkaround
from .initiate_root_cause import InitiateRootCause
from .escalate_incident import EscalateIncident
from .file_change_request import FileChangeRequest
from .file_rollback_request import FileRollbackRequest
from .record_metric_entry import RecordMetricEntry
from .generate_incident_summary import GenerateIncidentSummary
from .publish_kb_article import PublishKbArticle
from .schedule_pir_session import SchedulePirSession
from .pull_incident import PullIncident
from .pull_event_records import PullEventRecords
from .pull_escalations import PullEscalations
from .pull_communications import PullCommunications
from .pull_kb_articles import PullKbArticles
from .alter_client import AlterClient
from .alter_user_permissions import AlterUserPermissions
from .alter_product import AlterProduct
from .alter_component import AlterComponent
from .alter_subscription import AlterSubscription
from .alter_sla import AlterSla
from .alter_incident import AlterIncident
from .alter_escalation import AlterEscalation
from .alter_change_request import AlterChangeRequest
from .alter_rollback_request import AlterRollbackRequest
from .alter_rca import AlterRca
from .alter_communication import AlterCommunication
from .alter_kb_article import AlterKbArticle
from .alter_post_incident_review import AlterPostIncidentReview
from .flag_incident_resolved import FlagIncidentResolved
from .finalize_case import FinalizeCase
from .rate_severity import RateSeverity
from .confirm_approval_status import ConfirmApprovalStatus
from .write_audit_entry import WriteAuditEntry
from .route_to_human import RouteToHuman

ALL_TOOLS_INTERFACE_4 = [
    IdentifyEntities,
    RecordEventEntry,
    AssociateEventsOnce,
    RegisterCustomer,
    RegisterUser,
    OnboardSupplier,
    AddProductRecord,
    AddComponentRecord,
    ProvisionSubscription,
    SpecifySla,
    LogIncident,
    RecordCommunicationEntry,
    EnactWorkaround,
    InitiateRootCause,
    EscalateIncident,
    FileChangeRequest,
    FileRollbackRequest,
    RecordMetricEntry,
    GenerateIncidentSummary,
    PublishKbArticle,
    SchedulePirSession,
    PullIncident,
    PullEventRecords,
    PullEscalations,
    PullCommunications,
    PullKbArticles,
    AlterClient,
    AlterUserPermissions,
    AlterProduct,
    AlterComponent,
    AlterSubscription,
    AlterSla,
    AlterIncident,
    AlterEscalation,
    AlterChangeRequest,
    AlterRollbackRequest,
    AlterRca,
    AlterCommunication,
    AlterKbArticle,
    AlterPostIncidentReview,
    FlagIncidentResolved,
    FinalizeCase,
    RateSeverity,
    ConfirmApprovalStatus,
    WriteAuditEntry,
    RouteToHuman,
]
