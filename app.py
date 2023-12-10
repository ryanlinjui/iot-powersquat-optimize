from flask import Flask, request, abort
from linebot.v3.exceptions import (
    InvalidSignatureError
)
# import logging

from utils import (
    line_webhook
)
import os
import routes

# logging.basicConfig(
#     level = logging.DEBUG,
#     filename = "runtime.log",
#     filemode = "w",
#     format = "%(asctime)s %(levelname)s: %(message)s"
# )

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<h1>hello world</h1>"

@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    print(f"Request body: {body}")
    # logging.debug(f"Request body: {body}")

    # handle webhook body
    try:
        line_webhook.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "OK"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)