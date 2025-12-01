from dataclasses import asdict
from http import HTTPStatus

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from expenselog_api.models import Account


@pytest.mark.asyncio
async def test_create_account(client, session: AsyncSession, mock_db_time):
    with mock_db_time(model=Account) as time:
        response = client.post(
            '/users/',
            json={
                'username': 'teste',
                'email': 'test@example.com',
                'password': 'secret',
            },
        )

        account = await session.scalar(
            select(Account).where(Account.user_id == response.json()['id'])
        )

    assert asdict(account) == {
        'user_id': 1,
        'balance': 0.0,
        'total_income': 0.0,
        'total_expenses': 0.0,
        'id': 1,
        'created_at': time,
        'updated_at': time,
    }


def test_get_account(client, account, token):
    response = client.get(
        '/accounts/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user_id': account.user_id,
        'balance': 0.0,
        'total_income': 0.0,
        'total_expenses': 0.0,
        'id': 1,
    }


def test_increase_balance(client, account, token):
    response = client.put(
        '/accounts/increase_balance',
        headers={'Authorization': f'Bearer {token}'},
        params={'amount': 150.0},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user_id': account.user_id,
        'balance': 150.0,
        'total_income': 0.0,
        'total_expenses': 0.0,
        'id': account.id,
    }


def test_decrease_balance(client, account, token):
    response = client.put(
        '/accounts/decrease_balance',
        headers={'Authorization': f'Bearer {token}'},
        params={'amount': 150.0},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user_id': account.user_id,
        'balance': -150.0,
        'total_income': 0.0,
        'total_expenses': 0.0,
        'id': account.id,
    }


def test_increase_balance_invalid_amount(client, account, token):
    response = client.put(
        '/accounts/increase_balance',
        headers={'Authorization': f'Bearer {token}'},
        params={'amount': -50.0},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Amount must be greater than zero'}


def test_decrease_balance_invalid_amount(client, account, token):
    response = client.put(
        '/accounts/decrease_balance',
        headers={'Authorization': f'Bearer {token}'},
        params={'amount': -50.0},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Amount must be greater than zero'}


def test_increase_balance_with_nan_amount():
    account = Account(user_id=1, balance=100.0)

    result = account.increase_balance(float('NaN'))
    assert result is False


def test_decrease_balance_with_nan_amount():
    account = Account(user_id=1, balance=100.0)

    result = account.decrease_balance(float('NaN'))
    assert result is False
