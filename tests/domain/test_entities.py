from datetime import datetime, timezone
from uuid import uuid4
from src.domain.entities.case import Case
from src.domain.entities.client_tenant import ClientTenant
from src.domain.entities.system_connector import SystemConnector
from src.domain.entities.communication_channel import CommunicationChannel
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority
from src.domain.value_objects.connector_type import ConnectorType
from src.domain.value_objects.channel_type import ChannelType
from src.domain.value_objects.system_capability import SystemCapability
from src.domain.value_objects.channel_capability import ChannelCapability, NotificationType


def test_create_case():
    now = datetime.now(timezone.utc)
    case = Case(
        id=uuid4(),
        title="Test Case",
        description="A test cybersecurity case",
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
        client_tenant_id=uuid4(),
        created_at=now,
        updated_at=now,
    )
    assert case.status == CaseStatus.OPEN
    assert case.priority == CasePriority.HIGH
    assert case.assigned_to is None
    assert case.external_ids == {}
    assert case.notifications_sent == []


def test_create_client_tenant():
    now = datetime.now(timezone.utc)
    tenant = ClientTenant(
        id=uuid4(),
        name="ACME Corp",
        active=True,
        created_at=now,
        updated_at=now,
    )
    assert tenant.name == "ACME Corp"
    assert tenant.active is True
    assert tenant.system_connectors == []
    assert tenant.communication_channels == []


def test_create_system_connector():
    now = datetime.now(timezone.utc)
    connector = SystemConnector(
        id=uuid4(),
        name="ServiceNow Production",
        connector_type=ConnectorType.SERVICENOW,
        base_url="https://instance.service-now.com",
        credentials={"username": "admin", "password": "secret"},
        active=True,
        created_at=now,
        updated_at=now,
        capabilities=[SystemCapability.CREATE_CASE, SystemCapability.CLOSE_CASE],
    )
    assert connector.connector_type == ConnectorType.SERVICENOW
    assert SystemCapability.CREATE_CASE in connector.capabilities


def test_create_communication_channel():
    now = datetime.now(timezone.utc)
    channel = CommunicationChannel(
        id=uuid4(),
        name="Slack SOC",
        channel_type=ChannelType.SLACK,
        config={"webhook_url": "https://hooks.slack.com/xxx"},
        active=True,
        created_at=now,
        updated_at=now,
        capabilities=[ChannelCapability.MARKDOWN, ChannelCapability.SAME_THREAD],
    )
    assert channel.channel_type == ChannelType.SLACK
    assert ChannelCapability.MARKDOWN in channel.capabilities


def test_case_status_enum():
    assert CaseStatus.OPEN.value == "open"
    assert CaseStatus.IN_PROGRESS.value == "in_progress"
    assert CaseStatus.CLOSED.value == "closed"


def test_case_priority_enum():
    assert CasePriority.CRITICAL.value == "critical"
    assert CasePriority.LOW.value == "low"


def test_notification_type_enum():
    assert NotificationType.CASE_CREATED.value == "case_created"
    assert NotificationType.CASE_CLOSED.value == "case_closed"
