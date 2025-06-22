import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

import pyperclip
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, Controller
from browser_use.agent.views import ActionResult
from browser_use.browser import BrowserProfile, BrowserSession
from browser_use.browser.types import Page

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
	raise ValueError('GOOGLE_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

browser_profile = BrowserProfile(
	headless=False,
)
controller = Controller()


@controller.registry.action('Copy text to clipboard')
def copy_to_clipboard(text: str):
	pyperclip.copy(text)
	return ActionResult(extracted_content=text)


@controller.registry.action('Paste text from clipboard')
async def paste_from_clipboard(page: Page):
	text = pyperclip.paste()
	# send text to browser
	await page.keyboard.type(text)

	return ActionResult(extracted_content=text)


async def main():
	task = '複製 "twtrubiks github repo" 到剪貼簿, 然後去 google.com 貼上你剛剛複製的文字'
	browser_session = BrowserSession(browser_profile=browser_profile)
	await browser_session.start()
	agent = Agent(
		task=task,
		llm=llm,
		controller=controller,
		browser_session=browser_session,
	)

	await agent.run()
	await browser_session.stop()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())