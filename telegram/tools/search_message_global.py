from datetime import datetime
from typing import Type, List, Optional

from pydantic import BaseModel, Field

from telegram.tools.base import BaseTelegramTool


class SearchMessageGlobalInput(BaseModel):
    """Input for ClickTool."""
    search_text: str = Field(description="Search text. For retrieving last messages leave empty")
    limit: Optional[int] = Field(default=50, description="Limit of messages")


class Message(BaseModel):
    chat_id: int = Field(..., description="Id of the chat. chat_id")
    message_id: int = Field(..., description="Id of the message")
    text: str = Field(..., description="Message text")
    date: datetime = Field(..., description="Date of message")
    from_user_id: Optional[int] = Field(...,
                                        description="User ID of the sender. Can be none if its messsage in channel")
    from_user_name: Optional[str] = Field(...,
                                          description="User name of the sender. Can be none if its messsage in channel")


class SearchMessageGlobal(BaseTelegramTool):
    name = "SearchMessageGlobal"
    description = "Search message global. Can use if don't have specific chat"
    args_schema: Type[BaseModel] = SearchMessageGlobalInput

    async def _arun(self, search_text: str, limit: int = 50) -> List[Message]:
        messages: list[Message] = []
        async for message in self.client.search_global(query=search_text,
                                                       limit=limit):
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
