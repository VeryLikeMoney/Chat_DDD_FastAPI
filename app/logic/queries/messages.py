from dataclasses import dataclass
from typing import Any, Coroutine, Generic, Iterable

from domain.entities.messages import Chat, Message
from infra.repositories.filters.messages import GetMessagesFilters
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.exeptions.messages import ChatNotFoundExseption
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler

@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str

@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilters

@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler):
    chat_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository # TODO забирать сообщение отдельно
    
    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)
        
        if not chat: 
            raise ChatNotFoundExseption(chat_oid=query.chat_oid)
        
        return chat

@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    messages_repository: BaseMessagesRepository
    
    async def handle(self, query: GetMessagesQuery) -> Iterable[Message]:
        return await self.messages_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )