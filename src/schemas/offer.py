from marshmallow import fields

from . import BasicSchema


class OfferCreateSchema(BasicSchema):
    """Валидирование входных данных при создании объявления"""
    user_id = fields.Int(required=True)
    title = fields.Str(required=True)
    text = fields.Str(required=False)
