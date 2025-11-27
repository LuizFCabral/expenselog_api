from http import HTTPStatus


def test_root(client):
    response = client.get('/')

    assert response.json() == {'message': 'Welcome to the Expense Log API'}
    assert response.status_code == HTTPStatus.OK
