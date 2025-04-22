from http import HTTPStatus


class NotFoundError(Exception):
    def __init__(self, message: str = "Post", status_code: int = HTTPStatus.NOT_FOUND) -> None:
        self.message = "Not found [ " + str(message) + " ]"
        self.status_code = status_code


class ExistConflictError(Exception):
    def __init__(self, message: str = "Post", status_code: int = HTTPStatus.CONFLICT) -> None:
        self.message = "Exist Conflict [ " + str(message) + " ]"
        self.status_code = status_code


class UnprocessableContentError(Exception):
    def __init__(self, message: str = "Post", status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY) -> None:
        self.message = "Unprocessable Content [ " + str(message) + " ]"
        self.status_code = status_code
