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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()