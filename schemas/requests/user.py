from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RequestRegisterUserSchema(UserSchema):
    first_name = fields.Str(validate=validate.Length(min=2, max=20), required=True)
    last_name = fields.Str(validate=validate.Length(min=2, max=20), required=True)
    phone = fields.Str(validate=validate.Length(min=14, max=14), required=True)


class RequestLoginUserSchema(UserSchema):
    pass


class RequestRegisterComplainerSchema(RequestRegisterUserSchema):
    iban = fields.String(validate=validate.Length(min=14, max=22), required=True)
