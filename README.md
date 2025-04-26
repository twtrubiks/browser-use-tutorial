# 賦予瀏覽器 AI 大腦：深入 browser-use 的多模態自動化革命 🧠

* [Youtube Tutorial - 賦予瀏覽器 AI 大腦：深入 browser-use 的多模態自動化革命 🧠](https://youtu.be/IIt68zX6xq8)

今天介紹 [browser-use](https://github.com/browser-use/browser-use) 🤖

還有另一個 UI 版本 [web-ui](https://github.com/browser-use/web-ui)

這個項目是 AI 透過瀏覽器瀏覽（特別是大型語言模型 LLM，而且是**多模態模型**）,

然後透過 LLM 模擬人類的動作.

什麼是**多模態模型**, 指的是不同類型或形式的數據/資訊來源,

像是 文字 📝, 圖片 🖼️, 聲音 🔊 等等. 同時處理多種的能力.

它的運作方式大致如下 ⚙️

1.  **接收指令：** 你用自然語言描述想要執行的動作（例如：「點擊登入按鈕」、「在搜尋框輸入『天氣』」）。

2.  **理解畫面：** 它會擷取當前瀏覽器頁面的視覺資訊以及可能的網頁結構資訊。

3.  **AI 分析 (LLM)：** 將視覺資訊和你的指令一起傳送給多模態的 LLM。LLM 會像人一樣「看懂」畫面上的元素佈局和文字內容，理解你的意圖，並找出對應的操作目標（例如哪個按鈕是「登入」、哪個輸入框是「搜尋框」）。

4.  **執行動作：** AI 模型決定了要操作的元素和方式後，這個庫會轉換成實際的瀏覽器自動化指令（例如模擬點擊、輸入文字）。

關於速度部份 ⏱️

**這種透過視覺畫面反應的方式，通常在執行單一步驟時，會比傳統的自動化方法（例如使用 XPath 或 CSS Selector）來得慢。**

主要原因如下：

1. **畫面分析成本：** 分析圖像內容比直接透過程式碼（如 DOM 結構）查找元素要複雜得多，需要更多的計算資源。

2. **LLM 推理延遲 ⏳：** 將畫面資訊傳送給大型語言模型（通常是雲端服務），等待模型分析並回傳結果，這個過程包含網路延遲和模型本身的運算時間，通常需要數秒鐘。而傳統方法直接在本地端查找元素，速度非常快（毫秒級）。

3. **多步驟決策：** LLM 需要理解上下文、視覺佈局和指令意圖，這個「思考」過程比直接按選擇器定位元素要耗時。

**不過，雖然單一步驟較慢，但這種方法有其優勢**

1. **更強的適應性與穩定性：** 傳統方法依賴固定的選擇器（Selectors），一旦網站前端稍微修改，腳本就可能失效。而這種 AI 方法是理解頁面的「語意」和「視覺結構」，即使頁面有小幅變動，只要人類還能辨識，AI 通常也能正確找到目標元素.

2. **更自然的互動方式：** 可以用自然語言下指令，降低了編寫自動化腳本的門檻。

3. **處理視覺元素：** 對於沒有良好結構或難以用選擇器定位的元素，基於視覺的方法可能更有效。

## 開始把玩

這邊使用 `Python 3.12.3`

安裝 browser-use

```cmd
pip install browser-use
```

如果你要用其他的大語言模型, 像是我使用 GEMINI, 要多安裝

```cmd
pip install langchain-google-genai
```

如果你要用其他的 大語言模型, 可參考 [examples/models](https://github.com/browser-use/browser-use/tree/main/examples/models)

這裡提供很多, 連 [Ollama 簡介 🤖](https://github.com/twtrubiks/dify-ollama-docker-tutorial/blob/main/ollama.md) 也有.

安裝 Playwright

```cmd
playwright install chromium
```

之前有介紹過 [docker-selenium-tutorial](https://github.com/twtrubiks/docker-selenium-tutorial), 差異如下

**總結對比：**

| 特性             | Selenium                                  | Playwright                                       | 主要差異                                    |
| :--------------- | :---------------------------------------- | :----------------------------------------------- | :------------------------------------------ |
| **架構** | WebDriver (HTTP, 需 Driver)             | WebSocket/Pipe (直連, 管理瀏覽器)               | Playwright 連接更直接                       |
| **速度/穩定性** | 相對較慢，需手動精確管理等待              | **通常更快、更穩定 (內建自動等待)** | Playwright 在這方面優勢明顯                 |
| **API/易用性** | 強大但可能較冗長                          | **現代、直觀、簡潔** | Playwright API 更符合現代開發習慣             |
| **內建功能** | 核心功能為主，進階功能需額外設定          | **功能豐富 (網路、追蹤、多上下文)** | Playwright 開箱即用功能多                   |
| **設定** | 需管理 Driver 執行檔                      | **安裝指令自動下載瀏覽器** | Playwright 設定更簡單                       |
| **語言支援** | **極廣泛** | 主流語言 (TS/JS, Py, Java, .NET)                 | Selenium 支援更多語言                     |
| **瀏覽器支援** | 廣泛 (含舊版)                             | **現代主流瀏覽器 (Chromium, FF, WebKit)** | Selenium 支援更廣，Playwright 專注現代      |
| **社群/背景** | **歷史悠久，社群巨大，W3C標準** | 較新，Microsoft 維護，快速成長                  | Selenium 基礎更廣，Playwright 發展活躍        |

### 簡單範例 ✨

先來一個簡單的範例 [demo.py](demo.py) `python3 demo.py`

你會發現真的很強, 他有滾動功能, 自己透過網頁去思考, prompt 可參考 [prompts.py](https://github.com/browser-use/browser-use/blob/main/browser_use/agent/prompts.py)

### 驗證碼範例 🔒

這次呼叫自己本地的 chrome 瀏覽器.

解決驗證碼也可以 [demo-captcha.py](demo-captcha.py) `python3 demo-captcha.py`

如果你想看其他的範例, 可參考 [examples](https://github.com/browser-use/browser-use/tree/main/examples)

你會發現幾乎可以辦法任何事情.

也可以整合 slack 去呼叫 [examples/integrations](https://github.com/browser-use/browser-use/tree/main/examples/integrations/slack)

### twitter 自動發文 🐦

這邊不使用帳密登入, 使用 cookie 的方式.

先去下載 `Cookie-Editor` 擴充套件, 並且匯出為 json, 這邊保存為 `twitter_cookies.json`,

然後把裡面的 `"sameSite"` **全都** 修改為 `"Lax"` (不修改會錯誤)

```cmd
ERROR    [agent] ❌ Result failed 1/3 times:
BrowserContext.add_cookies: cookies[9].sameSite: expected one of (Strict|Lax|None)
```

[twitter_post_using_cookies.py](twitter_post_using_cookies.py) `python3 twitter_post_using_cookies.py`

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡 :laughing:

綠界科技ECPAY ( 不需註冊會員 )

![alt tag](https://payment.ecpay.com.tw/Upload/QRCode/201906/QRCode_672351b8-5ab3-42dd-9c7c-c24c3e6a10a0.png)

[贊助者付款](http://bit.ly/2F7Jrha)

歐付寶 ( 需註冊會員 )

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## 贊助名單

[贊助名單](https://github.com/twtrubiks/Thank-you-for-donate)

## License

MIT license
