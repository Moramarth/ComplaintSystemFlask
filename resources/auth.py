from flask import request
from flask_restful import Resource

from managers.user import ComplainerManager


class RegisterComplainer(Resource):
    # To-do:  data validation before token request
    def post(self):
        data = request.get_json()
        token = ComplainerManager.register(data)
        return {"token": token}, 201


class LoginComplainer(Resource):
    def post(self):
        data = request.get_json()
        token = ComplainerManager.login(data)
        return {"token": token, "role": "complainer"}
