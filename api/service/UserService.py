from repository.UserRepository import UserRepository
from model.User import User
from utils.dto import user_to_dto


class UserService:

    @staticmethod
    def get_user(user_id):
        user = UserRepository.find_by_id(user_id)
        return user_to_dto(user)

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.find_by_id(user_id)
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]

        UserRepository.save(user)
        return user_to_dto(user)

    @staticmethod
    def change_password(user, current, new):
        if not user.check_password(current):
            return False, "Current password is incorrect"

        user.set_password(new)
        UserRepository.save(user)
        return True, "Password updated"
    
    @staticmethod
    def register_user(data):
        if UserRepository.find_by_email(data["email"]):
            return False, "Email already in use"

        user = User(name=data["name"], email=data["email"])
        user.set_password(data["password"])
        UserRepository.save(user)
        return True, "User registered successfully"
