from __future__ import annotations

from fastapi import Depends
from api.dependencies.auth import get_current_user
from api.dependencies.use_cases import get_user_name_use_case
from app.use_cases.get_user_name import GetUserNameUseCase

async def name_user_auth(
        current_user: dict[str, object] = Depends(get_current_user),
        use_case = GetUserNameUseCase = Depends(get_user_name_use_case),
) -> str:
    return await use_case.execute(str(current_user.get("sub", "")))