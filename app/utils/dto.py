def user_to_dto(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "profile_image": getattr(user, "profile_image", None)
    }
    
def user_to_basic_dto(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "profile_image": getattr(user, "profile_image", None)
    }
