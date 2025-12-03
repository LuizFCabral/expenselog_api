from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from expenselog_api.models import Account, Transection, TransectionType, User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'test')
        )

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.asyncio
async def test_create_account(session: AsyncSession, mock_db_time, user):
    with mock_db_time(model=Account) as time:
        new_account = Account(user_id=user.id)

        session.add(new_account)
        await session.commit()

        account = await session.scalar(select(Account))

    assert asdict(account) == {
        'id': 1,
        'user_id': 1,
        'balance': 0.0,
        'total_income': 0.0,
        'total_expenses': 0.0,
        'created_at': time,
        'updated_at': time,
        'transections': [],
    }


@pytest.mark.asyncio
async def test_create_transection(
    session: AsyncSession, mock_db_time, account
):
    with mock_db_time(model=Transection) as time:
        new_transection = Transection(
            account_id=account.id,
            type=TransectionType.income,
            amount=100.0,
            description='Salary',
            balance_before=account.balance,
            balance_after=account.balance + 100.0,
        )

        session.add(new_transection)
        await session.commit()

        transection = await session.scalar(select(Transection))

    assert asdict(transection) == {
        'id': 1,
        'account_id': 1,
        'type': 'income',
        'amount': 100.0,
        'description': 'Salary',
        'balance_before': 0.0,
        'balance_after': 100.0,
        'created_at': time,
    }
