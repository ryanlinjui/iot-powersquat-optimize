# -*- coding: utf-8 -*-

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)
import os

from utils import *
from ..home import HomeMenu

class SkeletonMenu:
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

    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, DatabaseManager.STATE["skeleton"])
        reply_button_menu(token, SkeletonMenu.get_object())

    def callback(user_id:str, token:str, file:bytes):
        send_message(user_id, "正在上傳骨架影片\n請稍候......")
        filepath = save_tmp_file(file, "mp4")
        R2_Manager.upload(filepath)
        DatabaseManager.update_element(user_id, "skeleton", os.path.basename(filepath))
        SkeletonMenu.success(user_id, token)
        
    def success(user_id:str, token:str):
        send_message(user_id, "上傳骨架影片成功")
        HomeMenu.call(user_id, token)
    
    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳骨架影片一次")
        SkeletonMenu.call(user_id, token)