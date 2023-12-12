from flask import Blueprint, request, jsonify, abort
import threading

from utils import DatabaseManager

iot_receive_app = Blueprint("iot_receive", __name__)
tmp = {}

@iot_receive_app.route("/iot/<uuid>", methods=["POST"])
def _iot_receive(uuid:str):
    try:
        if request.is_json and DatabaseManager.get_state_by_iot(uuid) == DatabaseManager.STATE["analysis"]:
            tmp[uuid] = {}
            tmp[uuid]["event"] = threading.Event()
            tmp[uuid]["data"] = request.data.decode('utf-8')
            tmp[uuid]["event"].set()
            data_items = data_str.split("|")
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
            return jsonify({"status": "success"})
    finally:
        abort(403)