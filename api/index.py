from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('0iMXINLZV6RkNb+fgUbYeZsvM3ZYkXUPTTvVl6X610KeMN2SYLionwEmFkmEyV3pYKBjT4QPv6Ci6yX52t17bE9Ja1R62l1Vqn2CwvNxSjxHagi8TSOql/lwc/p+XNWFhTe9nNCurDAH06Lu0370TAdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('8b312c172bf6e9791e7c54abe218362e')

# 設定 OpenAI API 密鑰
# openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = "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"

# 輸入文本
input_text = "今天天氣很好，請用中文回答。請做一首跟天氣有關的詩"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 300

@app.route("/")
def home():
    return "LINE BOT API Server is running."

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 使用 GPT-3.5 模型生成文本
    response = openai.Completion.create(
        engine=model_engine,
        prompt=event.message.text,
        max_tokens=output_length,
    )

    # 取得生成的文本
    output_text = response.choices[0].text.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_text))

if __name__ == "__main__":
    app.run()