from sanic import Blueprint
from sanic.response import json

from schemas.offer import OfferCreateSchema
from marshmallow import ValidationError

bp = Blueprint('offers')


@bp.post('/create')
async def create_offer(request):
    try:
        offer_data = OfferCreateSchema().load(request.json)
    except ValidationError as error:
        return json(error.messages, status=400)

    return json(offer_data, status=200)


@bp.post('/')
async def read_offer(request):
    return json({'read offer': 'OK'}, status=200)
