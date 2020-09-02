from sanic import Blueprint
from sanic.response import json, empty

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
    return json({'read offer': 'OK'}, status=200)
