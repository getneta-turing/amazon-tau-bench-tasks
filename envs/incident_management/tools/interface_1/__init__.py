from .cancel_change_or_rollback import CancelChangeOrRollback
from .classify_severity import ClassifySeverity
from .create_approval_record import CreateApprovalRecord
from .create_audit_entry import CreateAuditEntry
from .create_change_request import CreateChangeRequest
from .create_escalation import CreateEscalation
from .create_incident import CreateIncident
from .create_knowledge_article import CreateKnowledgeArticle
from .create_metric_record import CreateMetricRecord
from .create_rollback_request import CreateRollbackRequest
from .create_workaround import CreateWorkaround
from .discover_entities import DiscoverEntities
from .generate_incident_report import GenerateIncidentReport
from .record_communication import RecordCommunication
from .resolve_and_close_incident import ResolveAndCloseIncident
from .schedule_pir import SchedulePIR
from .start_rca import StartRCA
from .update_incident_status import UpdateIncidentStatus
ALL_TOOLS_INTERFACE_1 = [
    CancelChangeOrRollback,
    ClassifySeverity,
    CreateApprovalRecord,
    CreateAuditEntry,
    CreateChangeRequest,
    CreateEscalation,
    CreateIncident,
    CreateKnowledgeArticle,
    CreateMetricRecord,
    CreateRollbackRequest,
    CreateWorkaround,
    DiscoverEntities,
    GenerateIncidentReport,
    RecordCommunication,
    ResolveAndCloseIncident,
    SchedulePIR,
    StartRCA,
    UpdateIncidentStatus

]
