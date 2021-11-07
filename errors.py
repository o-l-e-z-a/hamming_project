class NotValidCodeOptions(Exception):
    def __init__(self, value='Не корректные параметры кода'):
        self.msg = value

    def __str__(self):
        return self.msg
