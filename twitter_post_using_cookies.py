import asyncio
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
	raise ValueError('GOOGLE_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

file_path = os.path.join(os.path.dirname(__file__), 'twitter_cookies.json')
browser_session = BrowserSession(
	browser_profile=BrowserProfile(
		user_data_dir='~/.config/browseruse/profiles/default',
		cookies_file=file_path,
		# headless=False,  # Uncomment to see the browser
	)
)


async def main():
	agent = Agent(
		browser_session=browser_session,
		task='到 https://x.com, 發一篇文章, 內容是  browser-use 超神',
		llm=llm,
		max_actions_per_step=4,
	)
	await agent.run(max_steps=25)
	input('Press Enter to close the browser...')


if __name__ == '__main__':
	asyncio.run(main())
