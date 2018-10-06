from models.authentication.AdminModel import AdminModel
from werkzeug.security import safe_str_cmp

# We've transferred all of our DB operations to our user class
def authenticate(username,password):
    admin = AdminModel.findByUsername(username)
    if admin and safe_str_cmp(admin.password, password):
        return admin

def identity(payload):
    admin_id = payload["identity"]
    return AdminModel.findById(admin_id)
