from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from expenselog_api.database import get_session
from expenselog_api.models import Account, Transection, User
from expenselog_api.schemas.schemas import (
    AccountSchema,
    FilterPage,
    TransectionList,
)
from expenselog_api.security import get_current_account, get_current_user

router = APIRouter(prefix='/accounts', tags=['accounts'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentAccount = Annotated[Account, Depends(get_current_account)]
T_FilterPage = Annotated[FilterPage, Query()]


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


@router.get('/', response_model=AccountSchema)
async def get_account(
    account: CurrentAccount,
):
    return account


@router.put('/increase_balance', response_model=AccountSchema)
async def increase_balance(
    amount: float, account: CurrentAccount, session: Session
):

    if amount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Amount must be greater than zero',
        )

    account.increase_balance(amount)

    session.add(account)
    await session.commit()
    await session.refresh(account)

    return account


@router.put('/decrease_balance', response_model=AccountSchema)
async def decrease_balance(
    amount: float, account: CurrentAccount, session: Session
):
    if amount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Amount must be greater than zero',
        )
    account.decrease_balance(amount)

    session.add(account)
    await session.commit()
    await session.refresh(account)

    return account


@router.get('/transections', response_model=TransectionList)
async def list_transections(
    account: CurrentAccount,
    session: Session,
    filter: T_FilterPage,
):
    transections = await session.scalars(
        select(Transection)
        .where(Account.id == account.id)
        .order_by(Account.created_at.desc())
        .limit(filter.limit)
        .offset(filter.offset)
    )

    return {'transections': transections.all()}
