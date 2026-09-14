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
        encoded_image = ProfileImageService.get_profile_image_base64(user_id)
        return True, {
            "success": True,
            "message": "Profile image uploaded successfully",
            "profileImage": encoded_image,
        }

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
    def update_name(user_id, name):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return False, "User not found"

        name = (name or "").strip()
        if not name:
            return False, "Name is required"

        user.name = name
        UserRepository.save(user)
        return True, user_to_dto(user)

    @staticmethod
    def update_email(user_id, email):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return False, "User not found"

        email = (email or "").strip()
        if not email:
            return False, "Email is required"

        existing_user = UserRepository.find_by_email(email)
        if existing_user and existing_user.id != user_id:
            return False, "Email already in use"

        user.email = email
        UserRepository.save(user)
        return True, user_to_dto(user)

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
        """Public self-registration. Always creates a 'member' and requires a
        valid team invite code (see AuthService.register for the shared logic)."""
        from service.AuthService import AuthService
        result, error = AuthService.register(
            data.get("name"),
            data.get("email"),
            data.get("password"),
            data.get("invite_code"),
            profile_image,
        )
        if error:
            return False, error
        return True, result

    @staticmethod
    def create_user(creator, data):
        """Direct account creation by an Admin or Manager (no invite code needed).
        Admins can create Managers or Members. Managers can only create Members,
        and may optionally attach the new member to one of their teams."""
        if creator.role not in ("admin", "manager"):
            return False, "Not authorized to create users"

        role = (data.get("role") or "member").strip().lower()
        if role not in ("admin", "manager", "member"):
            return False, "Invalid role"
        if creator.role == "manager" and role != "member":
            return False, "Managers can only create members"

        required = ["name", "email", "password"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"

        email = data["email"].strip()
        if UserRepository.find_by_email(email):
            return False, "Email already in use"

        user = User(name=data["name"], email=email, role=role)
        user.set_password(data["password"])
        UserRepository.save(user)

        team_id = data.get("team_id")
        if team_id and role == "member":
            from service.TeamService import TeamService
            TeamService.add_member(creator, team_id, user.id)

        return True, user_to_dto(user)
