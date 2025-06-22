import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use.browser import BrowserSession
from browser_use.browser import BrowserProfile

from browser_use import Agent

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
	raise ValueError('GOOGLE_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


task_1 = """
瀏覽 https://excalidraw.com/.
選擇 pencil icon, 畫筆顏色選紅色,
從座標 (300,300), 畫一個 正方形
"""


browser_session = BrowserSession(
	browser_profile=BrowserProfile(
		downloads_path='~/Downloads',
		user_data_dir='~/.config/browseruse/profiles/default',
	)
)

async def run_search():
	agent = Agent(
		enable_memory=False,
		task=task_1,
		llm=llm,
		max_actions_per_step=1,
		use_vision=True,
		browser_session=browser_session,
	)

	await agent.run(max_steps=25)


if __name__ == '__main__':
	asyncio.run(run_search())