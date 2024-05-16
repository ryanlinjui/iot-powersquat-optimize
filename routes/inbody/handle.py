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
    send_message,
    save_tmp_file,
    send_object
)
from ..home import HomeMenu
from .process import inbody_recognition

class InbodyMenu:

    @staticmethod
    def get_object() -> TemplateSendMessage:
        return TemplateSendMessage(
            alt_text="Return",
            template=ButtonsTemplate(
                type="buttons",
                text="請上傳你的Inbody照片，如果要返回主頁面，請點擊按鈕返回",
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
        DatabaseManager.update_state(user_id, DatabaseManager.STATE["inbody"])
        reply_button_menu(token, InbodyMenu.get_object())

    @staticmethod
    def callback(user_id:str, token:str, file:bytes):
        send_message(user_id, "正在上傳Inbody照片\n請稍候......")
        json_file = inbody_recognition(save_tmp_file(file, "jpg"))
        json_filepath = save_tmp_file(json_file, "json")
        response = send_object(user_id, json_filepath, "inbody")
        
        if response == None: 
            InbodyMenu.exception(user_id, token)
            return
            
        InbodyMenu.success(user_id, token)
        
    @staticmethod
    def success(user_id:str, token:str):
        send_message(user_id, "上傳Inbody照片成功")
        HomeMenu.call(user_id, token)

    @staticmethod
    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳Inbody照片一次")
        InbodyMenu.call(user_id, token)