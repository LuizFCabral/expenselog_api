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


def test_add_transection(client, token, mock_db_time, account):
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
