def user_to_dto(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "profile_image": user.profile_image
    }
    
def user_to_basic_dto(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
