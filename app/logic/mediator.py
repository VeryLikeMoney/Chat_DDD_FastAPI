from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from domain.events.base import BaseEvent
from logic.commands.base import CR, CT, BaseCommand, CommandHandler
from logic.events.base import ER, ET, EventHandler
from logic.exeptions.mediator import CommandHandlersNotRegisteredException, EventHandlersNotRegisteredException

@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )
    
    def registrer_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].append(event_handlers)
        
    def registrer_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.events_map[command].extend(command_handlers)
    
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        event_type = events.__class__ 
        handlers = self.events_map.get(event_type)
        
        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)
        
        result = []
        
        for event in events:
            result.extend([await handler.handle(event) for handler in handlers])        

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__ 
        handlers = self.events_map.get(command_type)
        
        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)
        
        return [ await handler.handle(command) for handler in handlers ]
            
    
    