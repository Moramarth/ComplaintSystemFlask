from enum import Enum


class RoleType(Enum):
    approover = "approover"
    complainer = "complainer"
    admin = "admin"


class ComplaintState(Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"
