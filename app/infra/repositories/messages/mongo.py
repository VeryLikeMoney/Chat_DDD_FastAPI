from dataclasses import dataclass
from typing import Iterable
from motor.core import AgnosticClient
from domain.entities.messages import Chat, Message
from infra.repositories.filters.messages import GetMessagesFilters
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.converters import convert_chat_document_to_entity, convert_chat_entity_to_document, convert_message_entity_to_document, covert_message_document_to_entity

@dataclass
class BaseMongoDBReposity:
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str
    
    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

@dataclass
class MongoDBChatsRepository(BaseMongoDBReposity, BaseChatsRepository):         
    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={'title': title}))
    
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={'oid': oid})
        
        if not chat_document:
            return None
        
        return convert_chat_document_to_entity(chat_document)
    
    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(
            convert_chat_entity_to_document(chat),
        )

@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBReposity):   
    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_entity_to_document(message)
        )

    async def get_messages(self, chat_oid: str, filters: GetMessagesFilters) -> tuple[Iterable[Message], int]:
        find = {'chat_oid': chat_oid}
        cursor = self._collection.find(filter=find).skip(filters.offset).limit(filters.limit)
        
        messages = [
            covert_message_document_to_entity(message_document=message_document)
            async for message_document in cursor.skip(filters.offset).limit(filters.limit)
        ]
        count = await self._collection.count_documents(filter=find)
        
        return messages, count