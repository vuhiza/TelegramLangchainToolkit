from typing import Type, Optional

from pydantic import BaseModel, Field

from telegram.tools.base import BaseTelegramTool


class User(BaseModel):
    user_id: int = Field(..., description='The user id. user_id')
    first_name: Optional[str] = Field(..., alias='first_name', description='The user\'s first name.')
    last_name: Optional[str] = Field(..., alias='last_name', description='The user\'s last name.')
    username: Optional[str] = Field(..., alias='username', description='The user\'s username.')
    phone: Optional[str] = Field(..., description='The user\'s phone number.')
    is_bot: bool = Field(default=False, alias='is_bot', description='The user\'s is_bot.')


class GetUsersInput(BaseModel):
    user_ids: list[int] = Field(...,
                                description="user_id array. The user ids. If need to search for one user - just use it with one element in array")


class GetUsers(BaseTelegramTool):
    name = "GetUsers"
    description = "Get list of users by specified id's"
    args_schema: Type[BaseModel] = GetUsersInput

    async def _arun(self, user_ids: list[int]) -> list[User] | str:
        try:
            if not user_ids:
                return []

            results: list[User] = []
            for user in await self.client.get_users(user_ids):
                results.append(
                    User(
                        user_id=user.id,
                        username=user.username,
                        phone=user.phone_number,
                        is_bot=user.is_bot,
                        first_name=user.first_name,
                        last_name=user.last_name,
                    )
                )
            return results
        except Exception as e:
            return 'Users with such id don\'t exist: {}'.format(e)
