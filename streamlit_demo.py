"""
To use it, you'll need to install streamlit, and run with:

python -m streamlit run streamlit_demo.py

"""

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

import streamlit as st

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller


from langchain_google_genai import ChatGoogleGenerativeAI

from pydantic import SecretStr


load_dotenv()  # 確保 .env 檔案中有 GOOGLE_API_KEY=你的API金鑰
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError('GOOGLE_API_KEY is not set')


# Function to initialize the agent
def initialize_agent(query: str):
	llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=SecretStr(api_key))
	controller = Controller()
	browser = Browser(config=BrowserConfig())

	return Agent(
		task=query,
		controller=controller,
		llm=llm,
		browser=browser,
		use_vision=True,
		max_actions_per_step=1,
	)

# Streamlit UI
st.title('Automated Browser Agent with LLMs 🤖')

query = st.text_input('Enter your query:', '幫我查詢 twtrubiks 的 github 照片')
provider = st.radio('Select LLM Provider:', ['GEMINI'], index=0)

if st.button('Run Agent'):
	st.write('Initializing agent...')
	agent = initialize_agent(query)

	async def run_agent():
		with st.spinner('Running automation...'):
			await agent.run(max_steps=25)
		st.success('Task completed! 🎉')

	asyncio.run(run_agent())

	st.button('Close Browser', on_click=lambda: asyncio.run())
