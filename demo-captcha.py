import os
import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession

from dotenv import load_dotenv

from pydantic import SecretStr

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError('GOOGLE_API_KEY is not set')

browser_profile = BrowserProfile(
	# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
	executable_path='/opt/google/chrome/chrome', # 自己的瀏覽器路徑
	user_data_dir='~/.config/browseruse/profiles/default',
	headless=False,
)
browser_session = BrowserSession(browser_profile=browser_profile)


async def main():
    agent = Agent(
        enable_memory=False,
        task='到 https://captcha.com/demos/features/captcha-demo.aspx 解決驗證碼, 成功代表完成任務',

        # 效果比較好
        # llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro-preview-05-06", api_key=SecretStr(api_key)),

        # 效果比較差
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key)),

        browser_session=browser_session,
    )

    await agent.run()
    await browser_session.close()

if __name__ == '__main__':
	asyncio.run(main())
