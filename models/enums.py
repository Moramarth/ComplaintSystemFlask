from enum import Enum


class RoleType(Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"


class ComplaintState(Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
