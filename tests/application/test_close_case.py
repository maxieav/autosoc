import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4
from src.domain.entities.case import Case
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority
from src.application.use_cases.cases.close_case import CloseCaseUseCase


def make_case(**kwargs) -> Case:
    now = datetime.now(timezone.utc)
    defaults = dict(
        id=uuid4(),
        title="Test Case",
        description="Description",
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
        client_tenant_id=uuid4(),
        created_at=now,
        updated_at=now,
    )
    defaults.update(kwargs)
    return Case(**defaults)


@pytest.mark.asyncio
async def test_close_case_sets_closed_status():
    repo = AsyncMock()
    case = make_case()
    repo.get_by_id.return_value = case

    async def update_side_effect(c: Case) -> Case:
        return c

    repo.update.side_effect = update_side_effect
    use_case = CloseCaseUseCase(repo)
    result = await use_case.execute(case.id)
    assert result.status == CaseStatus.CLOSED


@pytest.mark.asyncio
async def test_close_case_not_found():
    repo = AsyncMock()
    repo.get_by_id.return_value = None
    use_case = CloseCaseUseCase(repo)
    with pytest.raises(ValueError, match="not found"):
        await use_case.execute(uuid4())
