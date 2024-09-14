from dataclasses import dataclass
from typing import Any, Coroutine, Generic

from domain.entities.messages import Chat
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.exeptions.messages import ChatNotFoundExseption
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler

@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str

@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler, Generic[QR, QT]):
    chat_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository # TODO забирать сообщение отдельно
    
    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=query.chat_oid)
        
        if not chat: 
            raise ChatNotFoundExseption(chat_oid=query.chat_oid)
        
        return chat