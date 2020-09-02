from typing import Optional, List

import peewee
from peewee import IntegrityError

from . import BasicModel
from database import manager


class User(BasicModel):
    """Модель пользователя. Нужна для ForeignKeyField"""
    user_id = peewee.AutoField()


class Offer(BasicModel):
    """Модель объявления"""
    offer_id = peewee.AutoField()
    user_id = peewee.ForeignKeyField(User, backref='offers', field='user_id')
    title = peewee.CharField()
    text = peewee.CharField()

    def __repr__(self):
        return f'Offer: {self.title} ({self.user_id})'

    @classmethod
    async def create(cls, data: dict) -> Optional['Offer']:
        try:
            return await manager.create(cls, **data)
        except IntegrityError:
            return None

    @staticmethod
    async def get_filtered(offer_id: int, user_id: int) -> List['Offer']:
        query = Offer.select()
        if offer_id is not None:
            query = query.where(Offer.offer_id == offer_id)
        if user_id is not None:
            query = query.where(Offer.user_id == user_id)
        query = query.order_by(Offer.user_id)

        offers = await manager.execute(query)

        return [offer.to_dict() for offer in offers]

    def to_dict(self) -> dict:
        return {
            'offer_id': self.offer_id,
            'user_id': self.user_id.user_id,
            'title': self.title,
            'text': self.text,
        }
