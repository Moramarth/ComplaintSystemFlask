from db import db
from models.enums import RoleType


class BaseUserModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class ComplainerModel(BaseUserModel):
    __tablename__ = "complainers"

    role = db.Column(db.Enum(RoleType), default=RoleType.complainer, nullable=False)


class ApproverModel(BaseUserModel):
    __tablename__ = "approvers"

    role = db.Column(db.Enum(RoleType), default=RoleType.approover, nullable=False)


class AdministratorModel(BaseUserModel):
    __tablename__ = "administrators"

    role = db.Column(db.Enum(RoleType), default=RoleType.admin, nullable=False)
