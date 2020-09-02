from typing import Optional

import peewee
from peewee import IntegrityError

from . import BasicModel
from database import manager


class User(BasicModel):
    """Модель пользователя. Нужна для ForeignKeyField"""
    user_id = peewee.AutoField()
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField(null=True)


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

    def to_dict(self):
        return {
            'offer_id': self.offer_id,
            'user_id': self.user_id.user_id,
            'title': self.title,
            'text': self.text,
        }
