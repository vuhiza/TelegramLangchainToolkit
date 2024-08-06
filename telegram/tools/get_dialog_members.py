from typing import Type, Optional

from pydantic import BaseModel, Field

from telegram.tools.base import BaseTelegramTool


class GetDialogMembersInput(BaseModel):
    chat_id: int = Field(..., description="Id of the chat. chat_id")
    search_text: str = Field(default='', description="Search text. For retrieving all members leave empty")
    limit: int = Field(default=50, description="Limit of messages")


class Member(BaseModel):
    chat_id: int = Field(..., description="Id of the chat. chat_id")
    user_id: int = Field(..., description="Id of the user")
    first_name: Optional[str] = Field(..., description="First name of the user")
    last_name: Optional[str] = Field(..., description="Last name of the user")
    username: Optional[str] = Field(..., description="Username of the user")


class GetDialogMembers(BaseTelegramTool):
    name = "GetDialogMembers"
    description = "Get list of dialog members in chat"

    args_schema: Type[BaseModel] = GetDialogMembersInput

    async def _get_chat_members(self, chat_id: int, search_text: str = '', limit: int = 10) -> list[Member]:
        members: list[Member] = []
        async for member in self.client.get_chat_members(chat_id=chat_id, query=search_text, limit=limit):
            members.append(
                Member(
                    chat_id=member.chat.id if member.chat else member.user.id,
                    user_id=member.user.id,
                    first_name=member.user.first_name,
                    last_name=member.user.last_name,
                    username=member.user.username,
                )
            )

        return members

    async def _arun(self, chat_id: int, search_text: str = '', limit: int = 10) -> list[Member] | str:
        try:
            return await self._get_chat_members(chat_id=chat_id, search_text=search_text, limit=limit)
        except Exception as e:
            # Mock
            return str(e)
