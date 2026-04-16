import io
from PIL import Image, ImageOps, UnidentifiedImageError
from model.UserProfileImage import UserProfileImage
from repository.UserProfileImageRepository import UserProfileImageRepository
import base64


class ProfileImageService:
    MAX_UPLOAD_BYTES = 2 * 1024 * 1024
    OUTPUT_SIZE = (100, 100)
    JPEG_QUALITY = 60

    @staticmethod
    def process_profile_image(file_storage):
        raw_data = file_storage.read()
        if not raw_data:
            return None, "Uploaded image is empty"

        if len(raw_data) > ProfileImageService.MAX_UPLOAD_BYTES:
            return None, "Profile image must be less than 2MB"

        try:
            with Image.open(io.BytesIO(raw_data)) as image:
                image = image.convert("RGB")
                resample_mode = getattr(Image, "Resampling", Image).LANCZOS
                image = ImageOps.fit(image, ProfileImageService.OUTPUT_SIZE, method=resample_mode)

                output = io.BytesIO()
                image.save(output, format="JPEG", quality=ProfileImageService.JPEG_QUALITY, optimize=True)
                return output.getvalue(), None
        except (UnidentifiedImageError, OSError, ValueError):
            return None, "Invalid image format"

    @staticmethod
    def save_for_user(user_id, image_bytes):
        existing = UserProfileImageRepository.find_by_user_id(user_id)
        if existing:
            existing.blob = image_bytes
            return UserProfileImageRepository.save(existing)

        profile_image = UserProfileImage(user_id=user_id, blob=image_bytes)
        return UserProfileImageRepository.save(profile_image)
    
    @staticmethod
    def get_profile_image_base64(user_id):
        profile_image = UserProfileImageRepository.find_by_user_id(user_id)
        if not profile_image or not profile_image.blob:
            return None
        return base64.b64encode(profile_image.blob).decode("utf-8")
