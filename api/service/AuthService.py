from repository.UserRepository import UserRepository
from model.User import User
from utils.dto import user_to_dto
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token


class AuthService:

    @staticmethod
    def register(name, email, password):
        if UserRepository.find_by_email(email):
            return None, "Email already registered"

        user = User(name=name, email=email)
        user.set_password(password)
        UserRepository.save(user)

        access = create_access_token(identity=str(user.id))
        refresh = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": user_to_dto(user)
        }, None

    @staticmethod
    def login(email, password):
        user = UserRepository.find_by_email(email)
        if not user or not user.check_password(password):
            return None, "Invalid credentials"

        access = create_access_token(identity=str(user.id))
        refresh = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": user_to_dto(user)
        }, None
