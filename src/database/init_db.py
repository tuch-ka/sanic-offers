from . import db
from models.offer import Offer


def create_tables():
    with db:
        db.create_tables([Offer, ])
