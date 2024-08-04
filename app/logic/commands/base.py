from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar, Generic

@dataclass(frozen=True)
class BaseCommand(ABC):
    ...

CT = TypeVar(name='CT',bound=BaseCommand)
CR = TypeVar(name='CR', bound=Any)

@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT]):
    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...
    

    
        