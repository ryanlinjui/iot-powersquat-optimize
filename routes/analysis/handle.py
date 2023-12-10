# -*- coding: utf-8 -*-

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)
import os

from utils import *
from ..home import HomeMenu

import time

class AnalysisMenu:
    def get_object() -> TemplateSendMessage:
        return TemplateSendMessage(
            alt_text="Return",
            template=ButtonsTemplate(
                type="buttons",
                text="請上傳你的深蹲影片後等候分析結果，如果要返回主頁面，請點擊按鈕返回",
                actions=[
                    PostbackAction(
                        label="返回主頁面",
                        data=DatabaseManager.STATE["return"]
                    )
                ]
            )
        )

    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, DatabaseManager.STATE["analysis"])
        reply_button_menu(token, AnalysisMenu.get_object())

    def callback(user_id:str, token:str, file:bytes):
        send_message(user_id, "正在開始分析，可能需要一些時間，完成時將會通知您，在此之前請勿做其他操作")
        filepath = save_tmp_file(file, "mp4")
        R2_Manager.upload(filepath)
        DatabaseManager.update_element(user_id, DatabaseManager.STATE["analysis"], os.path.basename(filepath))
        
        try:
            AnalysisMenu.analysis()
            AnalysisMenu.success(user_id, token, )
        except:
            AnalysisMenu.exception(user_id, token)
        
    def success(user_id:str, token:str, url:str):
        send_message(user_id, "分析完成，以下為分析影片:")
        send_video(user_id, url)
        HomeMenu.call(user_id, token)

    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳深蹲影片一次")  
        AnalysisMenu.call(user_id, token)

    def analysis():
        time.sleep(10)
        # TODO send video url to another server
        return