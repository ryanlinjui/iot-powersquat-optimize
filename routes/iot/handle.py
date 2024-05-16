# -*- coding: utf-8 -*-

import os

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)

from utils import (
    DatabaseManager,
    reply_button_menu,
    send_message
)
from ..home import HomeMenu

class IoTMenu:

    @staticmethod
    def get_object() -> TemplateSendMessage:
        return TemplateSendMessage(
            alt_text="Return",
            template=ButtonsTemplate(
                type="buttons",
                text="請輸入你的物聯網裝置UUID，如果要返回主頁面，請點擊按鈕返回",
                actions=[
                    PostbackAction(
                        label="返回主頁面",
                        data=DatabaseManager.STATE["return"]
                    )
                ]
            )
        )

    @staticmethod
    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, DatabaseManager.STATE["iot"])
        reply_button_menu(token, IoTMenu.get_object())

    @staticmethod
    def callback(user_id:str, token:str, uuid:str):
        send_message(user_id, "正在設定裝置UUID\n請稍候......")
        if (uuid in DatabaseManager.get_iot_uuid_list()) == False:
            
            IoTMenu.exception(user_id, token)
            return
        DatabaseManager.update_element(user_id, "sensor_uuid", uuid)
        IoTMenu.success(user_id, token)

    @staticmethod
    def success(user_id:str, token:str):
        send_message(user_id, "設定裝置UUID成功")
        HomeMenu.call(user_id, token)

    @staticmethod
    def exception(user_id:str, token:str):
        send_message(user_id, "不合法的UUID, 請再輸入一次")
        IoTMenu.call(user_id, token)
