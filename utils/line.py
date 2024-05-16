import os
import logging

from linebot import (
    LineBotApi,
    WebhookHandler
)
from linebot.models import (
    TextMessage,
    VideoSendMessage,
    TemplateSendMessage
)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
line_webhook = WebhookHandler(os.getenv("CHANNEL_SECRET"))

def reply_message(token:str, msg:str):
    line_bot_api.reply_message(
        token,
        messages=TextMessage(text=msg)
    )

def send_message(user_id:str, msg:str):
    line_bot_api.push_message(
        user_id,
        messages=TextMessage(text=msg)
    )

def reply_video(token:str, url:str, preview:str=None):
    logging.debug(f"Pass Function: reply_video, parameter: token: {token}, url: {url}, preview: {preview}")
    if preview is None: preview = url
    line_bot_api.reply_message(
        token,
        messages=VideoSendMessage(original_content_url=url, preview_image_url=preview)
    )

def send_video(user_id:str, url:str, preview:str=None):
    logging.debug(f"Pass Function: send_video, parameter: user_id: {user_id}, url: {url}, preview: {preview}")
    if preview is None: preview = url
    line_bot_api.push_message(
        user_id,
        messages=VideoSendMessage(original_content_url=url, preview_image_url=preview)
    )

def reply_button_menu(token:str, template:TemplateSendMessage):
    line_bot_api.reply_message(token, template)