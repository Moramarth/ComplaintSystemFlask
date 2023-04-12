from sqlalchemy import func

from db import db
from models.enums import ComplaintState


class ComplaintModel(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.Enum(ComplaintState), default=ComplaintState.pending, nullable=False)
    complainer_id = db.Column(db.Integer, db.ForeignKey("complainers.id"))
    complainer = db.relationship("ComplainerModel")