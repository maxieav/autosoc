from __future__ import annotations
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.database import get_db_session
from src.infrastructure.db.repositories.case_repository import CaseRepository
from src.infrastructure.db.repositories.client_tenant_repository import ClientTenantRepository
from src.infrastructure.db.repositories.system_connector_repository import SystemConnectorRepository
from src.infrastructure.db.repositories.communication_channel_repository import CommunicationChannelRepository
from src.infrastructure.ai_engine.ollama_adapter import OllamaAIEngine
from src.infrastructure.config import get_settings, Settings
from src.application.use_cases.cases.create_case import CreateCaseUseCase
from src.application.use_cases.cases.update_case import UpdateCaseUseCase
from src.application.use_cases.cases.close_case import CloseCaseUseCase
from src.application.use_cases.cases.reopen_case import ReopenCaseUseCase
from src.application.use_cases.cases.assign_case import AssignCaseUseCase
from src.application.use_cases.cases.get_case import GetCaseUseCase
from src.application.use_cases.cases.list_cases import ListCasesUseCase
from src.application.use_cases.tenants.create_tenant import CreateTenantUseCase
from src.application.use_cases.tenants.update_tenant import UpdateTenantUseCase
from src.application.use_cases.tenants.get_tenant import GetTenantUseCase
from src.application.use_cases.tenants.list_tenants import ListTenantsUseCase
from src.application.use_cases.connectors.register_system_connector import RegisterSystemConnectorUseCase
from src.application.use_cases.connectors.register_communication_channel import RegisterCommunicationChannelUseCase


def get_ai_engine(settings: Settings = Depends(get_settings)) -> OllamaAIEngine:
    return OllamaAIEngine(settings.ollama_base_url, settings.ollama_model)


def get_case_repo(session: AsyncSession = Depends(get_db_session)) -> CaseRepository:
    return CaseRepository(session)


def get_tenant_repo(session: AsyncSession = Depends(get_db_session)) -> ClientTenantRepository:
    return ClientTenantRepository(session)


def get_system_connector_repo(session: AsyncSession = Depends(get_db_session)) -> SystemConnectorRepository:
    return SystemConnectorRepository(session)


def get_communication_channel_repo(
    session: AsyncSession = Depends(get_db_session),
) -> CommunicationChannelRepository:
    return CommunicationChannelRepository(session)


def get_create_case_use_case(
    repo: CaseRepository = Depends(get_case_repo),
    ai: OllamaAIEngine = Depends(get_ai_engine),
) -> CreateCaseUseCase:
    return CreateCaseUseCase(repo, ai)


def get_update_case_use_case(repo: CaseRepository = Depends(get_case_repo)) -> UpdateCaseUseCase:
    return UpdateCaseUseCase(repo)


def get_close_case_use_case(repo: CaseRepository = Depends(get_case_repo)) -> CloseCaseUseCase:
    return CloseCaseUseCase(repo)


def get_reopen_case_use_case(repo: CaseRepository = Depends(get_case_repo)) -> ReopenCaseUseCase:
    return ReopenCaseUseCase(repo)


def get_assign_case_use_case(repo: CaseRepository = Depends(get_case_repo)) -> AssignCaseUseCase:
    return AssignCaseUseCase(repo)


def get_get_case_use_case(repo: CaseRepository = Depends(get_case_repo)) -> GetCaseUseCase:
    return GetCaseUseCase(repo)


def get_list_cases_use_case(repo: CaseRepository = Depends(get_case_repo)) -> ListCasesUseCase:
    return ListCasesUseCase(repo)


def get_create_tenant_use_case(repo: ClientTenantRepository = Depends(get_tenant_repo)) -> CreateTenantUseCase:
    return CreateTenantUseCase(repo)


def get_update_tenant_use_case(repo: ClientTenantRepository = Depends(get_tenant_repo)) -> UpdateTenantUseCase:
    return UpdateTenantUseCase(repo)


def get_get_tenant_use_case(repo: ClientTenantRepository = Depends(get_tenant_repo)) -> GetTenantUseCase:
    return GetTenantUseCase(repo)


def get_list_tenants_use_case(repo: ClientTenantRepository = Depends(get_tenant_repo)) -> ListTenantsUseCase:
    return ListTenantsUseCase(repo)


def get_register_system_connector_use_case(
    repo: SystemConnectorRepository = Depends(get_system_connector_repo),
) -> RegisterSystemConnectorUseCase:
    return RegisterSystemConnectorUseCase(repo)


def get_register_communication_channel_use_case(
    repo: CommunicationChannelRepository = Depends(get_communication_channel_repo),
) -> RegisterCommunicationChannelUseCase:
    return RegisterCommunicationChannelUseCase(repo)
