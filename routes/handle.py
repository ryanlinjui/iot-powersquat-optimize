from linebot.models import (
    TextMessage,
    ImageMessage,
    VideoMessage
)
from linebot.models.events import (
    MessageEvent, 
    PostbackEvent,
    FollowEvent,
    UnfollowEvent
)

from utils import *
from .exception import expection_replay
from .iot import IoTMenu
from .inbody import InbodyMenu
from .skeleton import SkeletonMenu
from .analysis import AnalysisMenu
from .home import HomeMenu

# TODO block user action for each menu case when user thread is running

@line_webhook.add(FollowEvent)
def handle_follow(event:FollowEvent):
    # reply home menu and create and inital data with user
    user_id = event.source.user_id
    token = event.reply_token

    DatabaseManager.insert_user(user_id)
    HomeMenu.call(user_id, token)

@line_webhook.add(UnfollowEvent)
def handle_unfollow(event:UnfollowEvent):
    # delete all data with user
    user_id = event.source.user_id
    print(user_id)
    DatabaseManager.delete_user(event.source.user_id)

@line_webhook.add(MessageEvent, message=TextMessage)
def handle_message(event:MessageEvent):
    # if state is iot, do it, otherwise, reply invaild msg and ask it again
    user_id = event.source.user_id
    token = event.reply_token
    message = event.message.text

    if DatabaseManager.get_state(user_id) == STATE["iot"]:
        IoTMenu.callback(user_id, token, message)
    else:
        expection_replay(user_id, token)

@line_webhook.add(MessageEvent, message=ImageMessage)
def handle_image(event:MessageEvent):
    # if state is inbody, do it, otherwise, reply invaild msg and ask it again
    user_id = event.source.user_id
    token = event.reply_token
    message_id = event.message.id 

    if DatabaseManager.get_state(user_id) == STATE["inbody"]:
        file_content = line_bot_api.get_message_content(message_id).content
        InbodyMenu.callback(user_id, token, file_content)
    else:
        expection_replay(user_id, token)

@line_webhook.add(MessageEvent, message=VideoMessage)
def handle_video(event:MessageEvent):
    # if state is skeloton or squat, do it, otherwise, reply invaild msg and ask it again
    user_id = event.source.user_id
    token = event.reply_token
    message_id = event.message.id

    if DatabaseManager.get_state(user_id) == STATE["skeleton"]:
        file_content = line_bot_api.get_message_content(message_id).content
        SkeletonMenu.callback(user_id, token, file_content)
    elif DatabaseManager.get_state(user_id) == STATE["analysis"]:
        file_content = line_bot_api.get_message_content(message_id).content
        AnalysisMenu.callback(user_id, token, file_content)
    else:
        expection_replay(user_id, token)
      
@line_webhook.add(PostbackEvent)
def handle_postback(event:PostbackEvent):
    # if state is home, do it, otherwise, reply invaild msg and ask it again
    user_id = event.source.user_id
    token = event.reply_token
    data = int(event.postback.data)

    if data == STATE["return"]: 
        HomeMenu.call(user_id, token)
    elif DatabaseManager.get_state(user_id) == STATE["home"]:
        if data == STATE["iot"]:
            IoTMenu.call(user_id, token)
        elif data == STATE["inbody"]:
            InbodyMenu.call(user_id, token)
        elif data == STATE["skeleton"]:
            SkeletonMenu.call(user_id, token)
        elif data == STATE["analysis"]:
            if DatabaseManager.check_element_exist(user_id, "inbody") and DatabaseManager.check_element_exist(user_id, "skeleton"):
                AnalysisMenu.call(user_id, token)
            else:
                HomeMenu.exception(user_id, token, STATE["analysis"])
    else:
        expection_replay(user_id, token)