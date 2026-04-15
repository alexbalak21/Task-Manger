def user_to_dto(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "createdAt": user.created_at.isoformat(),
        "updatedAt": user.updated_at.isoformat()
    }
    
def user_to_basic_dto(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }
