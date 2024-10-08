from dataclasses import dataclass

from logic.exeptions.base import LogicException

@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(LogicException):
    title: str
    
    @property
    def message(self):
        return f'Чат с таким названием "{self.title}" уже существует'


@dataclass(eq=False)
class ChatNotFoundExseption(LogicException):
    chat_oid: str
    
    @property
    def message(self):
        return f'Чат с таким {self.chat_oid=} не найден'