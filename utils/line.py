from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.models import (
    TextMessage,
    VideoSendMessage,
    TemplateSendMessage
)
import os

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
line_webhook = WebhookHandler(os.getenv("CHANNEL_SECRET"))

def reply_message(token:str, msg:str):
    line_bot_api.reply_message(
        token,
        messages=TextMessage(text=msg)
    )

def send_message(line_id:str, msg:str):
    line_bot_api.push_message(
        line_id,
        messages=TextMessage(text=msg)
    )

def reply_video(token:str, url:str, preview:str=None):
    if preview is None: preview = url
    line_bot_api.reply_message(
        token,
        messages=VideoSendMessage(original_content_url=url, preview_image_url=preview)
    )

def send_video(line_id:str, url:str, preview:str=None):
    line_bot_api.push_message(
        line_id,
        messages=VideoSendMessage(original_content_url=url, preview_image_url=preview)
    )

def reply_button_menu(token:str, template:TemplateSendMessage):
    line_bot_api.reply_message(token, template)