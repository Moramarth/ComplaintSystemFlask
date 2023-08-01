from marshmallow import fields

from marshmallow_enum import EnumField

from models import ComplaintState
from schemas.bases import BaseComplaintSchema


class ResponseComplaintSchema(BaseComplaintSchema):
    id = fields.Integer(required=True)
    status = EnumField(ComplaintState, by_value=True)
    created_on = fields.DateTime(required=True)
    photo_url = fields.URL(required=True)
