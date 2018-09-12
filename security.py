from models.UserModel import UserModel
from werkzeug.security import safe_str_cmp

# We've transferred all of our DB operations to our user class
def authenticate(username,password):
    user = UserModel.findByUsername(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload["identity"]
    return UserModle.findById(user_id)
