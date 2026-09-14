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


def team_to_dto(team, include_members=False):
    data = {
        "id": team.id,
        "name": team.name,
        "description": team.description,
        "created_by": team.created_by,
        "manager_name": team.manager.name if team.manager else None,
        "created_at": team.created_at.isoformat() if team.created_at else None,
        "member_count": len(team.members),
    }
    if include_members:
        data["members"] = [team_member_to_dto(m) for m in team.members]
    return data


def team_member_to_dto(team_member):
    return {
        "id": team_member.id,
        "team_id": team_member.team_id,
        "user_id": team_member.user_id,
        "name": team_member.user.name if team_member.user else None,
        "email": team_member.user.email if team_member.user else None,
        "joined_at": team_member.joined_at.isoformat() if team_member.joined_at else None,
    }


def invite_code_to_dto(invite_code):
    return {
        "id": invite_code.id,
        "code": invite_code.code,
        "team_id": invite_code.team_id,
        "is_active": invite_code.is_active,
        "created_at": invite_code.created_at.isoformat() if invite_code.created_at else None,
    }
