from repository.UserRepository import UserRepository
from model.User import User
from service.ProfileImageService import ProfileImageService
from utils.dto import user_to_dto


class UserService:

    @staticmethod
    def delete_profile_image(user_id):
        from repository.UserProfileImageRepository import UserProfileImageRepository
        profile_image = UserProfileImageRepository.find_by_user_id(user_id)
        if not profile_image:
            return False, "No profile image found for user"
        UserProfileImageRepository.delete(profile_image)
        return True, "Profile image deleted successfully"

    @staticmethod
    def upload_profile_image(user_id, profile_image):
        if not profile_image or not getattr(profile_image, "filename", ""):
            return False, "No profile image uploaded"

        processed_image, image_error = ProfileImageService.process_profile_image(profile_image)
        if image_error:
            return False, image_error

        ProfileImageService.save_for_user(user_id, processed_image)
        return True, "Profile image uploaded successfully"

    @staticmethod
    def get_all_users():
        profile_images = {img["id"]: img["image"] for img in ProfileImageService.get_all_profile_images()}
        users = UserRepository.get_all_basic()

        # users is a list of dicts, not User objects
        for user in users:
            user["profile_image"] = profile_images.get(user["id"])

        return users


    @staticmethod
    def get_user(user_id):
        user = UserRepository.find_by_id(user_id)
        user.profile_image = ProfileImageService.get_profile_image_base64(user_id)
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
    def register_user(data, profile_image=None):
        if UserRepository.find_by_email(data["email"]):
            return False, "Email already in use"

        processed_image = None
        if profile_image and getattr(profile_image, "filename", ""):
            processed_image, image_error = ProfileImageService.process_profile_image(profile_image)
            if image_error:
                return False, image_error

        user = User(name=data["name"], email=data["email"])
        user.set_password(data["password"])
        UserRepository.save(user)

        if processed_image:
            ProfileImageService.save_for_user(user.id, processed_image)
        return True, "User registered successfully"
