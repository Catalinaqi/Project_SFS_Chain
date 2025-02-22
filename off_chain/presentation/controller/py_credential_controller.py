from off_chain.service.py_credential_service import UserService


class UserController:
    """
    Controller managing user authentication from the UI.
    """

    @staticmethod
    def validate_login(username: str, password: str):
        return UserService.login(username, password)

    @staticmethod
    def register_user(user_data: dict):
        return UserService.register(user_data)
