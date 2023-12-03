# -*- coding: utf-8 -*-

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)
import os

from utils import (
    reply_button_menu,
    reply_message,
    send_message,
    DatabaseManager,
    STATE, COL
)
from ..home import HomeMenu

UUID_LIST = [
    "test1",
    "test2",
    "test3",
    "test4",
    "test5"
]

class IoTMenu:
    def get_object() -> TemplateSendMessage:
        return TemplateSendMessage(
            alt_text="Return",
            template=ButtonsTemplate(
                type="buttons",
                text="請輸入你的物聯網裝置UUID，如果要返回主頁面，請點擊按鈕返回",
                actions=[
                    PostbackAction(
                        label="返回主頁面",
                        data=STATE["return"]
                    )
                ]
            )
        )

    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, STATE["iot"])
        reply_button_menu(token, IoTMenu.get_object())

    def callback(user_id:str, token:str, uuid:str):
        if (uuid in UUID_LIST) == False:
            IoTMenu.exception(user_id, token)
            return

        DatabaseManager.update_element(user_id, COL[4], uuid)
        IoTMenu.success(user_id, token)

    def success(user_id:str, token:str):
        send_message(user_id, "設定裝置UUID成功")
        HomeMenu.call(user_id, token)

    def exception(user_id:str, token:str):
        send_message(user_id, "不合法的UUID, 請再輸入一次")
        IoTMenu.call(user_id, token)
