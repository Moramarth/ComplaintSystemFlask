from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complaint import ComplaintManager
from models import RoleType
from schemas.requests.complaint import RequestComplaintSchema
from schemas.response.complaint import ResponseComplaintSchema
from utils.decorators import validate_schema, permission_required


class ComplaintListCreate(Resource):
    @auth.login_required
    # @validate_schema(RequestComplaintSchema)
    def get(self):
        user = auth.current_user()
        complaints = ComplaintManager.get_all_complainer_claims(user)
        return ResponseComplaintSchema().dump(complaints, many=True)

    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(RequestComplaintSchema)
    def post(self):
        complainer = auth.current_user()
        data = request.get_json()
        complaint = ComplaintManager.create(data, complainer)
        return ResponseComplaintSchema().dump(complaint)


class ApproveComplaint(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def put(self, id_):
        ComplaintManager.approve(id_)
        return 200


class RejectComplaint(Resource):
    @auth.login_required
    @permission_required(RoleType.approver)
    def put(self, id_):
        ComplaintManager.reject(id_)
        return 200
