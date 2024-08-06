from typing import Any, Type

from pydantic import BaseModel, Field

from telegram.tools.base import BaseTelegramTool


class Chat(BaseModel):
    chat_id: int = Field()
    chat_type: str = Field()
    chat_name: str = Field()


class GetDialogsInput(BaseModel):
    limit: int = Field(default=50, description="Limit of messages")


class GetDialogs(BaseTelegramTool):
    name = "GetDialogs"
    description = "Get list of dialogs"
    args_schema: Type[BaseModel] = GetDialogsInput

    async def _arun(self, limit: int = 10, **kwargs: Any) -> list[Chat]:
        dialogs: list[Chat] = []
        async for dialog in self.client.get_dialogs(limit):
            dialogs.append(
                Chat(
                    chat_id=dialog.chat.id,
                    chat_type=dialog.chat.type.value,
                    chat_name=dialog.chat.title if dialog.chat.title else
                    f'{dialog.chat.first_name} {dialog.chat.last_name}',
                )

            )
        return dialogs
