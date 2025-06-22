import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError('GOOGLE_API_KEY is not set')

from browser_use import Agent
from browser_use.browser.profile import BrowserProfile
from browser_use.browser.session import BrowserSession

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

async def main():
	browser_session = BrowserSession(
		browser_profile=BrowserProfile(
			keep_alive=True,
			user_data_dir=None,
			headless=False,
            window_size={'width': 800, 'height': 600}
		)
	)
	await browser_session.start()

	task1 = '瀏覽 google'
	task2 = '瀏覽 yahoo'

	agent1 = Agent(
		task=task1,
		browser_session=browser_session,
		llm=llm,
	)
	agent2 = Agent(
		task=task2,
		browser_session=browser_session,
		llm=llm,
	)

	await asyncio.gather(agent1.run(), agent2.run())
	await browser_session.kill()


asyncio.run(main())