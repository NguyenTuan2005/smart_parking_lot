from services.AuthService import AuthService


class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
        self._current_user = None

    def authenticate(self, username: str, password: str):
        if not username or not password:
            return None
        return self.auth_service.login(username, password)
