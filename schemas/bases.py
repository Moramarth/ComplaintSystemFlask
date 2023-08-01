from marshmallow import Schema, fields


class BaseComplaintSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
