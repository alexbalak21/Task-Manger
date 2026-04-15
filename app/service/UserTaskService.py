from repository.UserTaskRepository import UserTaskRepository
from repository.UserRepository import UserRepository
from repository.TaskRepository import TaskRepository

class UserTaskService:
    @staticmethod
    def assign_user_to_task(user_id, task_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        task = TaskRepository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        UserTaskRepository.assign_user_to_task(user_id, task_id)
        return True

    @staticmethod
    def unassign_user_from_task(user_id, task_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        task = TaskRepository.get_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        UserTaskRepository.unassign_user_from_task(user_id, task_id)
        return True

    @staticmethod
    def get_users_for_task(task_id):
        return UserTaskRepository.get_users_for_task(task_id)

    @staticmethod
    def get_tasks_for_user(user_id):
        return UserTaskRepository.get_tasks_for_user(user_id)
