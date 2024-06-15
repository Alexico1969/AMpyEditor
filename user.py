from flask_login import UserMixin

class User(UserMixin):
    users = {}

    def __init__(self, id_, email):
        self.id = id_
        self.email = email

    @staticmethod
    def get(user_id):
        return User.users.get(user_id)

    @staticmethod
    def get_or_create(user_info):
        user_id = user_info['sub']
        if user_id not in User.users:
            user = User(user_id, user_info['email'])
            User.users[user_id] = user
        return User.users[user_id]
