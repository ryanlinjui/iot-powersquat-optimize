from flask import Flask, request, abort
from linebot.v3.exceptions import (
    InvalidSignatureError
)

from utils import (
    line_webhook
)
import os
import routes
from routes.iot.receive import iot_receive_app

app = Flask(__name__)
app.register_blueprint(iot_receive_app)

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

    # handle webhook body
    try:
        line_webhook.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "OK"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)