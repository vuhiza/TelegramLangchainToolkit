import asyncio

import pyrogram
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

from telegram.toolkit import TelegramToolkit

app_id = input("App ID:")
app_hash = input('App hash: ')
prompt = input('Prompt: ')
session_id = input('Session ID: ')


async def main():
    client = pyrogram.Client(session_id, takeout=False, api_hash=app_hash, api_id=app_id, sleep_threshold=30)
    await client.start()
    toolkit = TelegramToolkit(client=client)

    llm = ChatOpenAI(model='gpt-3.5-turbo-0125')

    agent_chain = initialize_agent(
        toolkit.get_tools(),
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=False,
    )

    result = await agent_chain.arun(
        prompt
    )
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
