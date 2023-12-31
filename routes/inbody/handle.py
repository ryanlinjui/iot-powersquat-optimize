# -*- coding: utf-8 -*-

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)
import os

from utils import *
from ..home import HomeMenu
from .process import inbody_recognition

class InbodyMenu:
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

    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, DatabaseManager.STATE["inbody"])
        reply_button_menu(token, InbodyMenu.get_object())

    def callback(user_id:str, token:str, file:bytes):
        send_message(user_id, "正在上傳Inbody照片\n請稍候......")
        json_file = inbody_recognition(save_tmp_file(file, "json"))
        json_filepath = save_tmp_file(json_file, "json")
        R2_Manager.upload(json_filepath)
        DatabaseManager.update_element(user_id, "inbody", os.path.basename(json_filepath))
        InbodyMenu.success(user_id, token)
        
    def success(user_id:str, token:str):
        send_message(user_id, "上傳Inbody照片成功")
        HomeMenu.call(user_id, token)

    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳Inbody照片一次")
        InbodyMenu.call(user_id, token)