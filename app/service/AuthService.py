from repository.UserRepository import UserRepository
from model.User import User
from service.ProfileImageService import ProfileImageService
from utils.dto import user_to_dto
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token


class AuthService:

    @staticmethod
    def register(name, email, password, profile_image=None):
        if UserRepository.find_by_email(email):
            return None, "Email already registered"

        processed_image = None
        if profile_image and getattr(profile_image, "filename", ""):
            processed_image, image_error = ProfileImageService.process_profile_image(profile_image)
            if image_error:
                return None, image_error

        user = User(name=name, email=email)
        user.set_password(password)
        UserRepository.save(user)

        if processed_image:
            ProfileImageService.save_for_user(user.id, processed_image)

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
        profile_image = ProfileImageService.get_profile_image_base64(user.id)
        user.profile_image = profile_image
        access = create_access_token(identity=str(user.id))
        refresh = create_refresh_token(identity=str(user.id))

        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": user_to_dto(user)
        }, None
