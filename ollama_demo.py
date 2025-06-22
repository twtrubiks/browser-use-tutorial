import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama
from browser_use import Agent

llm = ChatOllama(
	model='qwen3:4b', # 'qwen3:8b' GPU 如果不夠力會很慢
	num_ctx=32000,
)


async def main():

	task = """
	到 https://github.com/browser-use/browser-use 總結這篇文章, 並且用中文回答
	"""

	agent = Agent(task=task, llm=llm)
	await agent.run()

if __name__ == '__main__':
	asyncio.run(main())