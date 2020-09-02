from sanic import Blueprint
from sanic.response import json, empty, text

from schemas.offer import OfferCreateSchema
from marshmallow import ValidationError

from models.offer import Offer

bp = Blueprint('offers')


@bp.post('/create')
async def create_offer(request):
    """Создание объявления. TODO: добавить проверку авторизации"""
    try:
        offer_data = OfferCreateSchema().load(request.json)
    except ValidationError as error:
        return json(error.messages, status=400)

    offer = await Offer.create(data=offer_data)
    if offer is None:
        return empty(400)

    return json(offer.to_dict(), status=200)


@bp.post('/')
async def read_offer(request):
    request_json = request.json
    offer_id = request_json.get('offer_id', None)
    user_id = request_json.get('user_id', None)

    offers = await Offer.read_by_id(offer_id, user_id)

    return json(offers, status=200)
