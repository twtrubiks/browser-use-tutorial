import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


browser = Browser(config=BrowserConfig())
file_path = os.path.join(os.path.dirname(__file__), 'twitter_cookies.json')
browser_context = BrowserContext(
	config=BrowserContextConfig(cookies_file=file_path), browser=browser)


async def main():
	agent = Agent(
		browser_context=browser_context,
		task='到 https://x.com, 發一篇文章, 內容是  browser-use 超神',
		llm=llm,
		max_actions_per_step=4,
	)
	await agent.run(max_steps=25)
	input('Press Enter to close the browser...')


if __name__ == '__main__':
	asyncio.run(main())
