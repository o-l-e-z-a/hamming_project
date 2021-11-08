class NotValidCodeOptions(Exception):
    def __init__(self, value='Не корректные параметры кода') -> None:
        self.msg = value

    def __str__(self) -> str:
        return self.msg


class CheckEncodingError(Exception):
    def __init__(self, value='Синдром при проверке результата кодирования не равен 0') -> None:
        self.msg = value

    def __str__(self) -> str:
        return self.msg
