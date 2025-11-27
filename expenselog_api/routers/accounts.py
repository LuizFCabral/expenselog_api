from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from expenselog_api.database import get_session
from expenselog_api.models import Account, User
from expenselog_api.schemas.schemas import AccountSchema
from expenselog_api.security import get_current_user

router = APIRouter(prefix='/accounts', tags=['accounts'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


async def create_account(user_id: int, session: Session):
    account_db = Account(
        user_id=user_id,
        balance=0.0,
        total_income=0.0,
        total_expenses=0.0,
    )

    session.add(account_db)
    await session.commit()
    await session.refresh(account_db)

    return account_db


@router.get('/{user_id}', response_model=AccountSchema)
async def get_account(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not authorized to access this account',
        )

    account = await session.scalar(
        select(Account).where(Account.user_id == user_id)
    )
    return account
