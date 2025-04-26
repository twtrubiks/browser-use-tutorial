import os

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserConfig, Browser
import asyncio
from dotenv import load_dotenv

from pydantic import SecretStr

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError('GEMINI_API_KEY is not set')

browser = Browser(
	config=BrowserConfig(
		headless=False,
		disable_security=False,
        browser_binary_path='/opt/google/chrome/chrome', # 自己的瀏覽器路徑
	)
)

async def main():
    agent = Agent(
        task='go to https://captcha.com/demos/features/captcha-demo.aspx and solve the captcha',
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key)),
        browser=browser,
    )

    await agent.run()
    await browser.close()

if __name__ == '__main__':
	asyncio.run(main())
