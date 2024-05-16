import os
import logging
import shutil

from flask import Flask, request, abort
from linebot.v3.exceptions import (
    InvalidSignatureError
)

import routes
from routes.iot.receive import iot_receive_app
from utils import (
    line_webhook
)

logging.basicConfig(
    level = logging.DEBUG,
    filename = "runtime.log",
    filemode = "w",
    format = "%(asctime)s %(levelname)s: %(message)s"
)

app = Flask(__name__)
app.register_blueprint(iot_receive_app)

def initialize():
    tmp_folder_path = os.path.join(os.getcwd(), "tmp")
    if os.path.exists(tmp_folder_path):
        shutil.rmtree(tmp_folder_path)
    os.makedirs(tmp_folder_path)

@app.route("/", methods=["GET"])
def hello_world():
    return "<h1>hello world</h1>"

@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    logging.debug(f"Request body: {body}")

    # handle webhook body
    try:
        line_webhook.handle(body, signature)
    except InvalidSignatureError:
        logging.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "OK"

if __name__ == "__main__":
    initialize()
    app.run(host="0.0.0.0", port=8080, debug=True)