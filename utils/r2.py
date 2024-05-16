import os

import boto3
from botocore.client import Config
from dataplane import s3_upload

class R2_Manager:
    client_access_key = os.getenv("R2_ACCESS_KEY_ID")
    client_secret = os.getenv("R2_SECRET_ACCESS_KEY")
    connection_url = os.getenv("R2_CONNECTION")
    busket = os.getenv("R2_BUCKET")
    domain = os.getenv("R2_DOMAIN")
    s3_connect = boto3.client(
        "s3",
        endpoint_url=connection_url,
        aws_access_key_id=client_access_key,
        aws_secret_access_key=client_secret,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )

    @classmethod
    def upload(cls, filepath):
        UploadObject = open(filepath, "rb").read()
        s3_upload(Bucket=cls.busket,
            S3Client=cls.s3_connect,
            TargetFilePath=os.path.basename(filepath),
            UploadObject=UploadObject,
            UploadMethod="Object"
        )