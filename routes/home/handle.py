# -*- coding: utf-8 -*-

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)
import os

from utils import (
    reply_button_menu,
    send_message,
    STATE, COL,
    DatabaseManager
)

class HomeMenu:
    def get_object() -> TemplateSendMessage:
        return TemplateSendMessage(
            alt_text="HomeMenu",
            template=ButtonsTemplate(
                type="buttons",
                thumbnail_image_url="https://i.imgur.com/zFeydUT.jpg",
                title="歡迎來到深蹲硬舉姿勢改善小幫手分析系統",
                text="點選下方按鈕操作，上傳相關資料後即可開始分析",
                actions=[
                    PostbackAction(
                        label="我要註冊一個新的IoT設備(可選)",
                        data=STATE["iot"]
                    ),
                    PostbackAction(
                        label="我要上傳一個新的Inbody照片(必需)",
                        data=STATE["inbody"]
                    ),
                    PostbackAction(
                        label="我要上傳一個新的骨架影片(必需)",
                        data=STATE["skeleton"]
                    ),
                    PostbackAction(
                        label="開始分析",
                        data=STATE["analysis"]
                    )
                ]
            )
        )

    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, STATE["home"])
        reply_button_menu(token, HomeMenu.get_object())

    def exception(user_id:str, token:str, error_num:int):
        if error_num == STATE["analysis"]:
            send_message(user_id, "開始分析之前必須先上傳Inbody照片和骨架影片")
            HomeMenu.call(user_id, token)