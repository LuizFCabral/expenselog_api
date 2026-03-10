from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from expenselog_api.database import get_session
from expenselog_api.models import Account, Transection
from expenselog_api.schemas.schemas import TransectionPublic, TransectionSchema
from expenselog_api.security import get_current_account

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentAccount = Annotated[Account, Depends(get_current_account)]

router = APIRouter(prefix='/transections', tags=['transections'])


@router.post('/', response_model=TransectionPublic)
async def add_transection(
    account: CurrentAccount, transection: TransectionSchema, session: Session
):
    if transection.amount <= 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Amount must be greater than zero',
        )

    db_transection = Transection(
        account_id=account.id,
        type=transection.type,
        amount=transection.amount,
        description=transection.description,
        balance_before=account.balance,
        balance_after=account.balance + transection.amount,
    )
    if transection.type == 'income':
        account.increase_balance(transection.amount)
    elif transection.type == 'expense':
        account.decrease_balance(transection.amount)

    session.add(db_transection)
    session.add(account)
    await session.commit()
    await session.refresh(db_transection)

    return db_transection
