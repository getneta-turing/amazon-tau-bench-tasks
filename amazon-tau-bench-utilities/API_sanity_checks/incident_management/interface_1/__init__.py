
from .discover_entities import DiscoverEntities
from .create_event_record import CreateEventRecord
from .correlate_events_once import CorrelateEventsOnce
from .create_client import CreateClient
from .create_user import CreateUser
from .register_vendor import RegisterVendor
from .create_product import CreateProduct
from .create_component import CreateComponent
from .create_subscription import CreateSubscription
from .create_sla import CreateSla
from .create_incident import CreateIncident
from .record_communication import RecordCommunication
from .implement_workaround import ImplementWorkaround
from .start_rca import StartRca
from .create_escalation import CreateEscalation
from .create_change_request import CreateChangeRequest
from .create_rollback_request import CreateRollbackRequest
from .record_metric import RecordMetric
from .generate_incident_report import GenerateIncidentReport
from .create_kb_article import CreateKbArticle
from .create_post_incident_review import CreatePostIncidentReview
from .get_incident import GetIncident
from .get_event_records import GetEventRecords
from .get_escalations import GetEscalations
from .get_communications import GetCommunications
from .get_kb_articles import GetKbArticles
from .update_client import UpdateClient
from .update_user_permissions import UpdateUserPermissions
from .update_product import UpdateProduct
from .update_component import UpdateComponent
from .update_subscription import UpdateSubscription
from .update_sla import UpdateSla
from .update_incident import UpdateIncident
from .update_escalation import UpdateEscalation
from .update_change_request import UpdateChangeRequest
from .update_rollback_request import UpdateRollbackRequest
from .update_rca import UpdateRca
from .update_communication import UpdateCommunication
from .update_kb_article import UpdateKbArticle
from .update_post_incident_review import UpdatePostIncidentReview
from .resolve_incident import ResolveIncident
from .close_incident import CloseIncident
from .classify_severity import ClassifySeverity
from .check_approval import CheckApproval
from .log_audit_trail import LogAuditTrail
from .transfer_to_human import TransferToHuman

ALL_TOOLS_INTERFACE_1 = [
    DiscoverEntities,
    CreateEventRecord,
    CorrelateEventsOnce,
    CreateClient,
    CreateUser,
    RegisterVendor,
    CreateProduct,
    CreateComponent,
    CreateSubscription,
    CreateSla,
    CreateIncident,
    RecordCommunication,
    ImplementWorkaround,
    StartRca,
    CreateEscalation,
    CreateChangeRequest,
    CreateRollbackRequest,
    RecordMetric,
    GenerateIncidentReport,
    CreateKbArticle,
    CreatePostIncidentReview,
    GetIncident,
    GetEventRecords,
    GetEscalations,
    GetCommunications,
    GetKbArticles,
    UpdateClient,
    UpdateUserPermissions,
    UpdateProduct,
    UpdateComponent,
    UpdateSubscription,
    UpdateSla,
    UpdateIncident,
    UpdateEscalation,
    UpdateChangeRequest,
    UpdateRollbackRequest,
    UpdateRca,
    UpdateCommunication,
    UpdateKbArticle,
    UpdatePostIncidentReview,
    ResolveIncident,
    CloseIncident,
    ClassifySeverity,
    CheckApproval,
    LogAuditTrail,
    TransferToHuman,
]
