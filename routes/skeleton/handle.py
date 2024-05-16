# -*- coding: utf-8 -*-

import os
import requests

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)

from utils import (
    DatabaseManager,
    reply_button_menu,
    send_message,
    save_tmp_file,
    send_object,
    send_video
)
from ..home import HomeMenu

class SkeletonMenu:

    @staticmethod
    def get_object() -> TemplateSendMessage:
        return TemplateSendMessage(
            alt_text="Return",
            template=ButtonsTemplate(
                type="buttons",
                text="請上傳你的骨架影片，如果要返回主頁面，請點擊按鈕返回",
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
        DatabaseManager.update_state(user_id, DatabaseManager.STATE["skeleton"])
        reply_button_menu(token, SkeletonMenu.get_object())

    @staticmethod
    def callback(user_id:str, token:str, file:bytes):
        send_message(user_id, "正在上傳骨架影片\n請稍候......")
        skeleton_filepath = save_tmp_file(file, "mp4")
        response = send_object(user_id, skeleton_filepath, "skeleton")
        
        if response == None: 
            SkeletonMenu.exception(user_id, token)
            return

        SkeletonMenu.success(user_id, token)
        
    @staticmethod
    def success(user_id:str, token:str):
        send_message(user_id, "上傳骨架影片成功")
        HomeMenu.call(user_id, token)
    
    @staticmethod
    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳骨架影片一次")
        SkeletonMenu.call(user_id, token)