from dataclasses import dataclass

from logic.exeptions.base import LogicException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type : type
    
    @property
    def messsage(self):
        return f'Не удалось найти обрабодчики для события: {self.event_type}'

@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type : type
    
    @property
    def messsage(self):
        return f'Не удалось найти обрабодчики для команды: {self.command_type}'
