from sanic import Blueprint
from sanic.response import json

bp = Blueprint('offers')


@bp.post('/create')
async def create_offer(request):
    return json({'create offer': 'OK'}, status=200)


@bp.post('/')
async def read_offer(request):
    return json({'read offer': 'OK'}, status=200)
