from http import HTTPStatus

import factory
import factory.fuzzy

from expenselog_api.models import Transection, TransectionType


class TransectionFactory(factory.Factory):
    class Meta:
        model = Transection

    account_id = 1
    description = factory.Faker('text')
    amount = factory.Faker('pyfloat', right_digits=2)
    type = factory.fuzzy.FuzzyChoice(TransectionType)


def test_add_transection_income(client, token, mock_db_time, account):
    with mock_db_time(model=Transection) as time:
        response = client.post(
            '/transections/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'type': 'income',
                'amount': 150,
                'description': 'Test transection',
            },
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'account_id': 1,
        'amount': 150,
        'description': 'Test transection',
        'type': 'income',
        'created_at': time.isoformat(),
    }


def test_add_transection_expense(client, token, mock_db_time, account):
    with mock_db_time(model=Transection) as time:
        response = client.post(
            '/transections/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'type': 'expense',
                'amount': 150,
                'description': 'Test transection',
            },
        )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'account_id': 1,
        'amount': 150,
        'description': 'Test transection',
        'type': 'expense',
        'created_at': time.isoformat(),
    }


def test_add_transection_no_amount(client, token):
    response = client.post(
        '/transections/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'type': 'income',
            'amount': 0,
            'description': 'Test transection',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Amount must be greater than zero',
    }
