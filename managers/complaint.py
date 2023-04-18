from db import db
from models import ComplaintModel, ComplainerModel, ComplaintState, TransactionModel
from services.wise import WiseService


class ComplaintManager:
    @staticmethod
    def create(data, complainer):
        data["complainer_id"] = complainer.id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        db.session.flush()
        ComplaintManager.issue_transaction(data["amount"], complainer.first_name + " " + complainer.last_name,
                                           complainer.iban, complaint.id)
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

    @staticmethod
    def issue_transaction(amount, full_name, iban, complaint_id):
        wise_service = WiseService()
        quote_id = wise_service.create_quote(amount)
        recipient_id = wise_service.create_recipient_account(full_name, iban)
        transfer_id = wise_service.create_transfer(recipient_id, quote_id)
        data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": recipient_id,
            "amount": amount,
            "complaint_id": complaint_id,
        }
        transaction = TransactionModel(**data)
        db.session.add(transaction)
        db.session.flush()

