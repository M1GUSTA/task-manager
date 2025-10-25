class TaskNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class WrongCredentialsError(Exception):
    pass


class UsernameAlreadyExists(Exception):
    pass


class AccessDeniedError(Exception):
    pass
