from marshmallow import fields

from schemas.bases import BaseComplaintSchema


class RequestComplaintSchema(BaseComplaintSchema):
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)

