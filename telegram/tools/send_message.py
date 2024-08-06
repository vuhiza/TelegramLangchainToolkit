from typing import Type

from pydantic import BaseModel, Field

from telegram.tools.base import BaseTelegramTool


class SendMessageInput(BaseModel):
    chat_id: int = Field(...,
                         description="id of the chat you want to send messages to. It can be user_id or chat_id")
    text: str = Field(..., description="text of the message")


class SendMessage(BaseTelegramTool):
    name = "SendMessage"
    description = "SendMessage to a Telegram chat."
    args_schema: Type[BaseModel] = SendMessageInput

    async def _arun(self, chat_id: int, text: str):
        await self.client.send_message(
            chat_id=chat_id,
            text=text
        )
