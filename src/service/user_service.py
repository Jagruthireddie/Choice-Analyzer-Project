from src.dao import user_dao

def register_user(name, email, password, role="user"):
    return user_dao.create_user(name, email, password, role)

def login_user(email, password):
    user = user_dao.get_user_by_email(email)
    if not user or user["password"] != password:
        return None
    return user
