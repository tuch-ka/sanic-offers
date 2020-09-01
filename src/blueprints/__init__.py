from sanic import Blueprint

from .offers import bp as offer_bp


api = Blueprint.group(offer_bp, url_prefix='offer')
