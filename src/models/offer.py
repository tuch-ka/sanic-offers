import peewee

from . import BasicModel


class User(BasicModel):
    """Модель пользователя. Нужна для ForeignKeyField"""
    user_id = peewee.AutoField()
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField(null=True)


class Offer(BasicModel):
    """Модель объявления"""
    offer_id = peewee.AutoField()
    user_id = peewee.ForeignKeyField(User, backref='offers')
    title = peewee.CharField()
    text = peewee.CharField()

    def __repr__(self):
        return f'Offer: {self.title} ({self.user_id})'
