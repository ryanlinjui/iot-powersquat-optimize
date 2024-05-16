# -*- coding: utf-8 -*-

from utils import (
    send_message,
    DatabaseManager
)
from .iot import IoTMenu
from .inbody import InbodyMenu
from .skeleton import SkeletonMenu
from .analysis import AnalysisMenu
from .home import HomeMenu

EXPECTION = {
    DatabaseManager.STATE["home"]: HomeMenu.call,
    DatabaseManager.STATE["inbody"]: InbodyMenu.call,
    DatabaseManager.STATE["skeleton"]: SkeletonMenu.call,
    DatabaseManager.STATE["iot"]: IoTMenu.call,
    DatabaseManager.STATE["analysis"]: AnalysisMenu.call
}

def invaild_replay(user_id:str, token:str):
    state = DatabaseManager.get_state(user_id)
    send_message(user_id, "不合法操作，請對系統友善一點")
    EXPECTION[state](user_id, token)

def expection_send(user_id:str):
    send_message(user_id, "未知錯誤情況發生，請再試一次")

__all__ = [
    "invaild_replay",
    "expection_send"
]
