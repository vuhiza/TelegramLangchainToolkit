from datetime import datetime
from typing import Type, List, Optional

from pydantic import BaseModel, Field

from telegram.tools.base import BaseTelegramTool


class SearchMessageInDialogInput(BaseModel):
    """Input for ClickTool."""
    chat_id: int = Field(..., description="Id of the chat. chat_id")
    user_id: Optional[int] = Field(default=None,
                                   description="Id of the sender. user_id. Use only if you need message from some user")
    search_text: str = Field(default='', description="Search text. For retrieving last messages leave empty")
    offset: int = Field(default=0, description="Offset from start of message")
    limit: int = Field(default=50, description="Limit of messages")


class Message(BaseModel):
    chat_id: int = Field(..., description="Id of the chat. chat_id")
    message_id: int = Field(..., description="Id of the message")
    text: str = Field(..., description="Message text")
    date: datetime = Field(..., description="Date of message")
    from_user_id: Optional[int] = Field(...,
                                        description="User ID of the sender. Can be none if its messsage in channel")
    from_user_name: Optional[str] = Field(...,
                                          description="User name of the sender. Can be none if its messsage in channel")


class SearchMessageInDialog(BaseTelegramTool):
    name = "SearchMessageInDialog"
    description = ("Search message in some chat. chat_id required parameter"
                   "For retrieve last messages leave query as empty string")
    args_schema: Type[BaseModel] = SearchMessageInDialogInput

    async def _search_messages(self, chat_id: int, user_id: int = None, search_text: str = '',
                               offset: int = 0, limit: int = 50) -> List[Message]:
        messages: list[Message] = []
        async for message in self.client.search_messages(chat_id=chat_id,
                                                         from_user=user_id,
                                                         query=search_text,
                                                         limit=limit,
                                                         offset=offset):
            if message.text or message.caption:
                messages.append(
                    Message(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        text=message.text or message.caption,
                        date=message.date,
                        from_user_id=message.from_user.id if message.from_user else None,
                        from_user_name=f'{message.from_user.first_name} {message.from_user.last_name}' if message.from_user else None
                    )
                )
        return messages

    async def _arun(self, chat_id: int, user_id: int = None, search_text: str = '',
                    offset: int = 0, limit: int = 50) -> List[Message] | str:
        try:
            return await self._search_messages(chat_id, user_id, search_text, offset, limit)
        except Exception as e:
            # Mock
            return str(e)
