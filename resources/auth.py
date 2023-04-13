from flask import request
from flask_restful import Resource

from managers.user import ComplainerManager
from schemas.requests.user import RequestRegisterUserSchema, RequestLoginUserSchema
from utils.decorators import validate_schema


class RegisterComplainer(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {"token": token}, 201


class LoginComplainer(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {"token": token, "role": "complainer"}
