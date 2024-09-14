from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.values.messages import Text, Title
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exeptions.messages import ChatNotFoundExseption, ChatWithThatTitleAlreadyExistsException

@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str

@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chats_repository: BaseChatsRepository
    
    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chats_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExistsException(command.title)
        
        title = Title(value=command.title)
        
        new_chat =  Chat.create_chat(title=title)
        await self.chats_repository.add_chat(new_chat)
        
        return new_chat

@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str 

@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Chat]):
    chats_repository: BaseChatsRepository
    message_repository: BaseMessagesRepository
    
    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
        
        if not chat:
            raise ChatNotFoundExseption(chat_oid=command.chat_oid)
        
        message = Message(text=Text(value=command.text), chat_oid=command.chat_oid)
        chat.add_message(message)
        await self.message_repository.add_message(message=message)
        
        return message
        
        