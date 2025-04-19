import os

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv

from pydantic import SecretStr

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')


async def main():
    agent = Agent(
        task="幫我找到 github twtrubiks 的 linux 教學, 找出 zsh 的部份, 幫我整理重點",
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key)),
    )

    await agent.run()

if __name__ == '__main__':
	asyncio.run(main())
