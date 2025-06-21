import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
	raise ValueError('GOOGLE_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

browser_session = BrowserSession(
	browser_profile=BrowserProfile(
		downloads_path=os.path.join(os.getcwd(), 'downloads'),
		user_data_dir='~/.config/browseruse/profiles/default',
	)
)

task ="""
	- 到 https://github.com/fastfetch-cli/fastfetch/releases/tag/2.44.0
	- 下載並保存 **fastfetch-linux-aarch64.deb**
"""

async def run_download():
	agent = Agent(
		enable_memory=False,
		task=task,
		llm=llm,
		max_actions_per_step=8,
		use_vision=True,
		browser_session=browser_session,
	)
	await agent.run(max_steps=25)
	await browser_session.close()


if __name__ == '__main__':
	asyncio.run(run_download())
