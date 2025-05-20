import os

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, BrowserConfig, Browser
import asyncio
from dotenv import load_dotenv

from pydantic import SecretStr

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError('GOOGLE_API_KEY is not set')

browser = Browser(
	config=BrowserConfig(
		headless=False,
		disable_security=False,
        browser_binary_path='/opt/google/chrome/chrome', # 自己的瀏覽器路徑
	)
)

async def main():
    agent = Agent(
        task='到 https://captcha.com/demos/features/captcha-demo.aspx 解決驗證碼, 成功代表完成任務',

        # 效果比較好
        # llm=ChatGoogleGenerativeAI(model="gemini-2.5-pro-preview-05-06", api_key=SecretStr(api_key)),

        # 效果比較差
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key)),

        browser=browser,
    )

    await agent.run()
    await browser.close()

if __name__ == '__main__':
	asyncio.run(main())
