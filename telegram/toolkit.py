from typing import Type, cast, List

import pyrogram
from langchain_core.tools import BaseToolkit, BaseTool
from pydantic import Extra

from telegram.tools.base import BaseTelegramTool
from .tools import GetDialogs, SearchMessageInDialog, GetDialogMembers, GetUsers, SendMessage, SearchMessageGlobal


class TelegramToolkit(BaseToolkit):
    client: pyrogram.Client

    class Config:
        extra = Extra.forbid
        arbitrary_types_allowed = True

    def get_tools(self) -> list[BaseTool]:
        tool_classes: list[Type[BaseTelegramTool]] = [
            GetDialogs,
            GetDialogMembers,
            SearchMessageInDialog,
            GetUsers,
            SendMessage,
            SearchMessageGlobal
        ]

        tools = [
            tool_cls.from_client(
                client=self.client
            )
            for tool_cls in tool_classes
        ]
        return cast(List[BaseTool], tools)
