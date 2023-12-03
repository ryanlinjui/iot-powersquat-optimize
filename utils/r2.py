from dataplane import s3_upload
import boto3
from botocore.client import Config
import os

from dotenv import load_dotenv
load_dotenv()

class R2_Manager:
    ClientAccessKey = os.getenv("R2_ACCESS_KEY_ID")
    ClientSecret = os.getenv("R2_SECRET_ACCESS_KEY")
    ConnectionUrl = os.getenv("R2_CONNECTION")
    Bucket = os.getenv("R2_BUCKET")
    domain = os.getenv("R2_DOMAIN")
    S3Connect = boto3.client(
        "s3",
        endpoint_url=ConnectionUrl,
        aws_access_key_id=ClientAccessKey,
        aws_secret_access_key=ClientSecret,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )
        
    @classmethod
    def upload(cls, filepath):
        UploadObject = open(filepath, "rb").read()
        s3_upload(Bucket=cls.Bucket,
            S3Client=cls.S3Connect,
            TargetFilePath=os.path.basename(filepath),
            UploadObject=UploadObject,
            UploadMethod="Object"
        )

if __name__ == "__main__":
    R2_Manager.upload("./tmp/output.mov")