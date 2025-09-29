from .add_audit_entry import AddAuditEntry
from .add_knowledge_article import AddKnowledgeArticle
from .add_metric import AddMetric
from .add_workaround import AddWorkaround
from .begin_rca import BeginRCA
from .cancel_change_request import CancelChangeRequest
from .change_incident_status import ChangeIncidentStatus
from .create_incident_report import CreateIncidentReport
from .find_entities import FindEntities
from .log_approval import LogApproval
from .log_communication import LogCommunication
from .open_incident import OpenIncident
ALL_TOOLS_INTERFACE_2 = [
    AddAuditEntry,
    AddKnowledgeArticle,
    AddMetric,
    AddWorkaround,
    BeginRCA,
    CancelChangeRequest,
    ChangeIncidentStatus,
    CreateIncidentReport,
    FindEntities,
    LogApproval,
    LogCommunication,
    OpenIncident
    
]
