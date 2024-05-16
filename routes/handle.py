import logging

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

from utils import (
    line_webhook,
    line_bot_api,
    DatabaseManager
)
from .exception import (
    invaild_replay,
    expection_send
)
from .iot import IoTMenu
from .inbody import InbodyMenu
from .skeleton import SkeletonMenu
from .analysis import AnalysisMenu
from .home import HomeMenu

def lock_event(func):
    def wrapper(*args, **kwargs):
        user_id = args[0].source.user_id
        if DatabaseManager.is_user_event_active(user_id) == False:
            DatabaseManager.reverse_event_status(user_id)
            logging.debug(f"User status lock: {user_id}")
            try:
                func(args[0])
            except Exception as e:
                logging.error(f"Exception: {e}, user_id: {user_id}")
                expection_send(user_id)
                raise(e)
            finally:
                DatabaseManager.reverse_event_status(user_id)
                logging.debug(f"User status unlock: {user_id}")
    return wrapper

@line_webhook.add(FollowEvent)
def handle_follow(event:FollowEvent):
    # reply home menu and create and inital data with user
    logging.debug(f"FollowEvent: {event.source.user_id}")
    
    user_id = event.source.user_id
    token = event.reply_token

    DatabaseManager.insert_user(user_id)
    HomeMenu.call(user_id, token)
    

@line_webhook.add(UnfollowEvent)
def handle_unfollow(event:UnfollowEvent):
    # delete all data with user
    logging.debug(f"UnfollowEvent: {event.source.user_id}")

    DatabaseManager.delete_user(event.source.user_id)

@line_webhook.add(MessageEvent, message=TextMessage)
@lock_event
def handle_message(event:MessageEvent):
    # if state is iot, do it, otherwise, reply invaild msg and ask it again
    logging.debug(f"MessageEvent: {event.source.user_id}")

    user_id = event.source.user_id
    token = event.reply_token
    message = event.message.text

    if DatabaseManager.get_state(user_id) == DatabaseManager.STATE["iot"]:
        IoTMenu.callback(user_id, token, message)
    else:
        invaild_replay(user_id, token)

@line_webhook.add(MessageEvent, message=ImageMessage)
@lock_event
def handle_image(event:MessageEvent):
    # if state is inbody, do it, otherwise, reply invaild msg and ask it again
    logging.debug(f"ImageEvent: {event.source.user_id}")

    user_id = event.source.user_id
    token = event.reply_token
    message_id = event.message.id 

    if DatabaseManager.get_state(user_id) == DatabaseManager.STATE["inbody"]:
        file_content = line_bot_api.get_message_content(message_id).content
        InbodyMenu.callback(user_id, token, file_content)
    else:
        invaild_replay(user_id, token)

@line_webhook.add(MessageEvent, message=VideoMessage)
@lock_event
def handle_video(event:MessageEvent):
    # if state is skeloton or analysis, do it, otherwise, reply invaild msg and ask it again
    logging.debug(f"VideoEvent: {event.source.user_id}")

    user_id = event.source.user_id
    token = event.reply_token
    message_id = event.message.id

    if DatabaseManager.get_state(user_id) == DatabaseManager.STATE["skeleton"]:
        file_content = line_bot_api.get_message_content(message_id).content
        SkeletonMenu.callback(user_id, token, file_content)
    elif DatabaseManager.get_state(user_id) == DatabaseManager.STATE["analysis"]:
        file_content = line_bot_api.get_message_content(message_id).content
        AnalysisMenu.callback(user_id, token, file_content)
    else:
        invaild_replay(user_id, token)

@line_webhook.add(PostbackEvent)
@lock_event
def handle_postback(event:PostbackEvent):
    # if state is home, do it, otherwise, reply invaild msg and ask it again
    logging.debug(f"PostbackEvent: {event.source.user_id}")

    user_id = event.source.user_id
    token = event.reply_token
    data = event.postback.data

    if data == DatabaseManager.STATE["return"]: 
        HomeMenu.call(user_id, token)
    elif DatabaseManager.get_state(user_id) == DatabaseManager.STATE["home"]:
        if data == DatabaseManager.STATE["iot"]:
            IoTMenu.call(user_id, token)
        elif data == DatabaseManager.STATE["inbody"]:
            InbodyMenu.call(user_id, token)
        elif data == DatabaseManager.STATE["skeleton"]:
            SkeletonMenu.call(user_id, token)
        elif data == DatabaseManager.STATE["analysis"]:
            if DatabaseManager.check_element_exist(user_id, "inbody") and DatabaseManager.check_element_exist(user_id, "skeleton"):
                AnalysisMenu.call(user_id, token)
            else:
                HomeMenu.exception(user_id, token)
    else:
        invaild_replay(user_id, token)