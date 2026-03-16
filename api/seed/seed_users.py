from model.User import User
from repository.UserRepository import UserRepository


def seed_users():
    # Admin user
    admin_email = "john.doe@example.com"
    admin = UserRepository.find_by_email(admin_email)
    if not admin:
        admin = User(
            name="John Doe",
            email=admin_email,
            role="admin"
        )
        admin.set_password("password@1234")
        UserRepository.save(admin)
        print("Seeded admin user:", admin_email)

    # Regular user
    user_email = "alex.smith@example.com"
    user = UserRepository.find_by_email(user_email)
    if not user:
        user = User(
            name="Alex Smith",
            email=user_email,
            role="user"
        )
        user.set_password("password@5678")
        UserRepository.save(user)
        print("Seeded regular user:", user_email)
