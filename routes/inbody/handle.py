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
    STATE, COL,
    R2_Manager,
    save_tmp_file
)
from ..home import HomeMenu

from .process import inbody_recognition

from utils import create_tmp_filename

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
                        data=STATE["return"]
                    )
                ]
            )
        )

    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, STATE["inbody"])
        reply_button_menu(token, InbodyMenu.get_object())

    def callback(user_id:str, token:str, file:bytes):
        img_filepath = save_tmp_file(file, "jpg")
        # json_file = inbody_recognition(img_filepath)
        json_filepath = create_tmp_filename("json")
        # R2_Manager.upload(json_filepath)
        DatabaseManager.update_element(user_id, COL[1], json_filepath)
        InbodyMenu.success(user_id, token)
        
        # except
            # InbodyMenu.exception(user_id, token)
            # return

    def success(user_id:str, token:str):
        send_message(user_id, "上傳Inbody照片成功")
        HomeMenu.call(user_id, token)

    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳Inbody照片一次")
        InbodyMenu.call(user_id, token)