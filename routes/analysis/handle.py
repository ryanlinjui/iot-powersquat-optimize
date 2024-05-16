# -*- coding: utf-8 -*-

import os
import time

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackAction
)
import requests

from utils import (
    DatabaseManager,
    reply_button_menu,
    send_message,
    save_tmp_file,
    send_object,
    send_video
)
from ..home import HomeMenu

class AnalysisMenu:

    @staticmethod
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

    @staticmethod
    def call(user_id:str, token:str):
        DatabaseManager.update_state(user_id, DatabaseManager.STATE["analysis"])
        reply_button_menu(token, AnalysisMenu.get_object())

    @staticmethod
    def callback(user_id:str, token:str, file:bytes):
        # analysis video
        send_message(user_id, "正在開始分析，可能需要一些時間，完成時將會通知您，在此之前請勿做其他操作")

        analysis_src_video_filepath = save_tmp_file(file, "mp4")
        
        response = send_object(user_id, analysis_src_video_filepath, "analysis_src")
        if response == "":
            AnalysisMenu.exception(user_id, token)
            return

        analysis_result_video_filepath = AnalysisMenu._send_analysis_request(user_id)
        if analysis_result_video_filepath == "": 
            AnalysisMenu.exception(user_id, token)
            return

        R2_Manager.upload(analysis_result_video_filepath)
        DatabaseManager.update_element(user_id, "analysis_result", os.path.basename(analysis_result_video_filepath))
        AnalysisMenu.success(user_id, token, os.getenv("ACCESS_DOMAIN") + os.path.basename(analysis_result_video_filepath))
        
    @staticmethod
    def success(user_id:str, token:str, url:str):
        send_message(user_id, "分析完成，以下為分析影片:")
        send_video(user_id, url)
        HomeMenu.call(user_id, token)

    @staticmethod
    def exception(user_id:str, token:str):
        send_message(user_id, "有些錯誤發生了, 請再次上傳深蹲影片")  
        AnalysisMenu.call(user_id, token)

    @staticmethod
    def _send_analysis_request(user_id:str) -> str:
        request_data = {
            "id": user_id,
            "inbody": DatabaseManager.get_element(user_id, "inbody"),
            "skeleton": DatabaseManager.get_element(user_id, "skeleton"),
            "analysis_src": DatabaseManager.get_element(user_id, "analysis_src"),
            "sensor_data": DatabaseManager.get_element(user_id, "sensor_data")
        }

        try:
            logging.debug(f"Request to analysis server: {request_data}")
            analysis_response : requests.Response = requests.post(
                os.getenv("ANALYSIS_SERVER_URL"),
                json=request_data
            )
            
            logging.debug(f"Respnse from analysis server: {response}")

            if analysis_response.status_code != 200:
                logging.error(f"Error issue occur when analysis video\nstatus code: {analysis_response.status_code}")        
                return ""
            else:
                DatabaseManager.update_element(user_id, element, filepath)

            analysis_result_video_filepath = save_tmp_file(analysis_response.content, "mp4")
            return analysis_result_video_filepath
        
        except Exception as e:
            logging.error(f"Error issue occur when analysis video: {e}")
            return ""