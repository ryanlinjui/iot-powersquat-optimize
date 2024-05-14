from flask import Blueprint, request, jsonify, abort
import json
import os
import logging

from utils import (
    DatabaseManager,
    save_tmp_file,
    R2_Manager
)

iot_receive_app = Blueprint("iot_receive", __name__)
tmp = {}

@iot_receive_app.route("/iot/<uuid>", methods=["POST"])
def _iot_receive(uuid:str):
    try:
        data_items = request.data.decode("utf-8").split("|")
        result_list = []
        for data_item in data_items:
            if len(data_item) < 5: continue
            values = data_item.split(",")
            values = [float(value) for value in values]

            data_dict = {
                "gyroX": values[0],
                "gyroY": values[1],
                "gyroZ": values[2],
                "accelX": values[3],
                "accelY": values[4],
                "accelZ": values[5],
                "pitch": values[6],
                "roll": values[7],
                "yaw": values[8],
                "timestamp": int(values[9])
            }
            result_list.append(data_dict)
        
        IMU_data = {
            "data": result_list
        }
        IMU_data_path = save_tmp_file(json.dumps(IMU_data).encode(), "json")
        user_id = DatabaseManager.get_user_id_by_sensor_uuid(uuid)
        DatabaseManager.update_element(user_id, "sensor_data", os.path.basename(IMU_data_path))
        R2_Manager.upload(IMU_data_path)
        return jsonify({"status": "success"})
    except Exception as e:
        logging.error(f"Error: {e}")
        abort(403)