import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4
from src.domain.entities.case import Case
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority
from src.application.dtos.case_dtos import UpdateCaseDTO
from src.application.use_cases.cases.update_case import UpdateCaseUseCase


def make_case(**kwargs) -> Case:
    now = datetime.now(timezone.utc)
    defaults = dict(
        id=uuid4(),
        title="Original Title",
        description="Original description",
        status=CaseStatus.OPEN,
        priority=CasePriority.MEDIUM,
        client_tenant_id=uuid4(),
        created_at=now,
        updated_at=now,
    )
    defaults.update(kwargs)
    return Case(**defaults)


@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    case = make_case()
    repo.get_by_id.return_value = case

    async def update_side_effect(c: Case) -> Case:
        return c

    repo.update.side_effect = update_side_effect
    return repo, case


@pytest.mark.asyncio
async def test_update_case_title(mock_repo):
    repo, original = mock_repo
    use_case = UpdateCaseUseCase(repo)
    dto = UpdateCaseDTO(title="Updated Title")
    result = await use_case.execute(original.id, dto)
    assert result.title == "Updated Title"


@pytest.mark.asyncio
async def test_update_case_not_found():
    repo = AsyncMock()
    repo.get_by_id.return_value = None
    use_case = UpdateCaseUseCase(repo)
    with pytest.raises(ValueError, match="not found"):
        await use_case.execute(uuid4(), UpdateCaseDTO(title="New"))


@pytest.mark.asyncio
async def test_update_case_partial(mock_repo):
    repo, original = mock_repo
    use_case = UpdateCaseUseCase(repo)
    dto = UpdateCaseDTO(priority=CasePriority.CRITICAL)
    result = await use_case.execute(original.id, dto)
    assert result.priority == CasePriority.CRITICAL
    assert result.title == original.title
