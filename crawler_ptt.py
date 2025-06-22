import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from browser_use import Agent, Controller
from browser_use.browser import BrowserProfile, BrowserSession

from pydantic import BaseModel
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
	raise ValueError('GOOGLE_API_KEY is not set')

# llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-preview-05-20', api_key=SecretStr(api_key))
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

browser_profile = BrowserProfile(
	# executable_path='/opt/google/chrome/chrome', # 自己的瀏覽器路徑
	# user_data_dir='~/.config/browseruse/profiles/default',
)
browser_session = BrowserSession(browser_profile=browser_profile)


class Post(BaseModel):
	title: str
	url: str
	images: list[str]

class Posts(BaseModel):
	posts: list[Post]

controller = Controller(output_model=Posts)

@controller.action('Save models', param_model=Posts)
def save_posts(parsed_posts: Posts):
	with open('crawler_ptt.txt', 'a') as f:
		for parsed in parsed_posts.posts:
			f.write('\n--------------------------------\n')
			f.write(f'Title:            {parsed.title}\n')
			f.write(f'url:              {parsed.url}\n')
			for image in parsed.images:
				f.write(f'Image:         {str(image)}\n')

async def main():

	task = """
	- 瀏覽 https://www.ptt.cc/bbs/Beauty/index3930.html

	- 如果跳出同意或離開, 請選擇同意

	- 點選任意1篇文章瀏覽, 找到文章內網址結尾是符合圖片的的網址

	- 總共瀏覽兩篇文章, 完成任務
	"""

	agent = Agent(
		task=task, llm=llm, controller=controller,
		browser_session=browser_session, validate_output=False)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed_posts: Posts = Posts.model_validate_json(result)

		for parsed in parsed_posts.posts:
			print('\n--------------------------------')
			print(f'Title:            {parsed.title}')
			print(f'url:              {parsed.url}')
			for image in parsed.images:
				print(f'Image:         {image}')


if __name__ == '__main__':
	asyncio.run(main())