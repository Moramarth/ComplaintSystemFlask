from resources.auth import RegisterComplainer, LoginComplainer
from resources.complaint import ComplaintListCreate, ApproveComplaint, RejectComplaint

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login"),
    (ComplaintListCreate, "/complainers/complaints"),
    (ApproveComplaint, "/approvers/complaints/<int:id_>/approve"),
    (RejectComplaint, "/approvers/complaints/<int:id_>/reject"),
)