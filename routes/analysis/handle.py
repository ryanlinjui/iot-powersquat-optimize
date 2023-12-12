# -*- coding: utf-8 -*-

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)
import os
import requests

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
        # analysis video
        send_message(user_id, "正在開始分析，可能需要一些時間，完成時將會通知您，在此之前請勿做其他操作")

        analysis_src_video_filepath = save_tmp_file(file, "mp4")
        R2_Manager.upload(analysis_src_video_filepath)
        DatabaseManager.update_element(user_id, "inbody", os.path.basename(analysis_src_video_filepath))

        try:
            AnalysisMenu.analysis(
                user_id=user_id,
                inbody_filepath=DatabaseManager.get_element(user_id, "inbody"),
                skeleton_filepath=DatabaseManager.get_element(user_id, "skeleton"),
                src_video_filepath=DatabaseManager.get_element(user_id, "analysis_src"),
                sensor_data_filepath=DatabaseManager.get_element(user_id, "sensor_data")
            )

            AnalysisMenu.success(user_id, token, analysis_result_url)
        except:
            AnalysisMenu.exception(user_id, token)
        
    def success(user_id:str, token:str, url:str):
        send_message(user_id, "分析完成，以下為分析影片:")
        send_video(user_id, url)
        HomeMenu.call(user_id, token)

    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳深蹲影片")  
        AnalysisMenu.call(user_id, token)

    def analysis(user_id:str, inbody_filepath:str, skeleton_filepath:str, src_video_filepath:str, sensor_data_filepath:str):
        request_data = {}
        request_data["inbody"] =  os.getenv("ACCESS_DOMAIN") + inbody_filepath
        request_data["skeleton"] = os.getenv("ACCESS_DOMAIN") + skeleton_filepath
        request_data["analysis_src"] = os.getenv("ACCESS_DOMAIN") + src_video_filepath
        request_data["sensor_data"] = os.getenv("ACCESS_DOMAIN") + sensor_data_filepath

        response = requests.post(os.getenv("ANALYSIS_SERVER_URL"), json=request_data)
        if response.status_code == 200:
            analysis_video_filepath = save_tmp_file(response.content, "mp4")
            R2_Manager.upload(analysis_video_filepath)
            DatabaseManager.update_element(user_id, "analysis_result", os.path.basename(analysis_video_filepath))
        else:
            raise(f"Error issue occur when analysis video\nstatus code: {response.status_code}")
        return os.getenv("ACCESS_DOMAIN") + analysis_video_filepath