from db import db
from models import ComplaintModel, ComplainerModel, ComplaintState


class ComplaintManager:
    @staticmethod
    def create(data, complainer_id):
        data["complainer_id"] = complainer_id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        db.session.flush()
        return complaint

    @staticmethod
    def get_all_complainer_claims(user):
        if isinstance(user, ComplainerModel):
            return ComplaintModel.query.filter_by(complainer_id=user.id).all()
        return ComplaintModel.query.all()

    @staticmethod
    def approve(id_):
        ComplaintModel.query.filter_by(id=id_).update({"status": ComplaintState.approved})

    @staticmethod
    def reject(id_):
        ComplaintModel.query.filter_by(id=id_).update({"status": ComplaintState.rejected})
