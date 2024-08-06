from abc import ABC
from typing import Any

import pyrogram
from langchain_core.tools import BaseTool


class BaseTelegramTool(BaseTool, ABC):
    client: pyrogram.Client

    def _run(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> Any:
        raise NotImplementedError('Only async calls are implemented.')

    @classmethod
    def from_client(cls, client: pyrogram.Client) -> 'BaseTelegramTool':
        """Instantiate the tool."""
        return cls(client=client)
