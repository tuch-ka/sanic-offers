import json
from unittest.mock import patch

import pytest
import peewee

from app import create_app
from auth import create_token
from models.offer import Offer


@pytest.yield_fixture
def app():
    application = create_app()
    yield application


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))


async def returning_created_offer(data) -> Offer:
    return Offer(**data)


async def returning_none(data: None) -> None:
    return None


def mock_related_instance(*args, **kwargs):
    def user_id():
        pass
    user_id.user_id = 0
    return user_id


async def mock_offer_get_filtered(*args, **kwargs):
    return []


#########
# Tests #
#########


class TestOfferCreation(object):
    """
    POST offer/create
    """
    cookies = {
        'token': create_token({'user_id': 0})
    }

    async def test_offer_create_no_auth(self, test_cli):
        """
        Создание объявления без авторизации
        """
        offer_data = dict()
        response = await test_cli.post('/offer/create', data=json.dumps(offer_data))
        assert response.status == 401

    async def test_offer_create_no_data(self, test_cli):
        """
        Создание объявления с пустым запросом
        """
        offer_data = dict()
        response = await test_cli.post('/offer/create', data=json.dumps(offer_data), cookies=self.cookies)
        assert response.status == 400

    @patch.object(Offer, 'create', returning_created_offer)
    async def test_offer_create_not_owner(self, test_cli):
        """
        Создание объявления с чужим user_id
        """
        offer_data = {
            'user_id': 1,
            'title': 'title',
            'text': 'text',
        }
        response = await test_cli.post('/offer/create', data=json.dumps(offer_data), cookies=self.cookies)
        assert response.status == 403

    @patch.object(Offer, 'create', returning_none)
    async def test_offer_create_no_user_id(self, test_cli):
        """
        Создание объявления без user_id
        """
        offer_data = {
            'title': 'title',
            'text': 'text',
        }
        response = await test_cli.post('/offer/create', data=json.dumps(offer_data), cookies=self.cookies)
        assert response.status == 400

    @patch.object(Offer, 'create', returning_created_offer)
    @patch.object(peewee.ForeignKeyAccessor, '__get__', mock_related_instance)
    async def test_offer_create_good_data(self, test_cli):
        """
        Создание объявления
        """
        offer_data = {
            'user_id': 0,
            'title': 'title',
            'text': 'text',
        }
        response = await test_cli.post('/offer/create', data=json.dumps(offer_data), cookies=self.cookies)
        assert response.status == 200

        response_json = await response.json()
        assert response_json.get('title') == offer_data['title']


@patch.object(Offer, 'get_filtered', mock_offer_get_filtered)
class TestOfferRead(object):

    async def test_offer_read_no_data(self, test_cli):
        """
        Пустое тело
        """
        response = await test_cli.post('/offer')
        assert response.status == 200

        response_json = await response.json()
        assert isinstance(response_json, list)

    async def test_offer_read_empty_data(self, test_cli):
        """
        Пустой запрос
        """
        response = await test_cli.post('/offer', data={})
        assert response.status == 200

    async def test_offer_read_bad_data(self, test_cli):
        """
        Плохой запрос
        """
        response = await test_cli.post('/offer', data=json.dumps({'user_id': -1}))
        assert response.status == 200
