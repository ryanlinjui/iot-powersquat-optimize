from google.cloud import vision
from google.oauth2 import service_account
from io import BytesIO
from os import getenv

class ImageDetection:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            getenv("GCLOUD_CREDENTIALS_PATH"),
            scopes=['https://www.googleapis.com/auth/cloud-platform'],
        )
        self.client = vision.ImageAnnotatorClient(credentials=credentials)

    def run(self, image):
        image_data = BytesIO()
        image.save(image_data, format="JPEG")
        image = vision.Image(content=image_data.getvalue())
        response = self.client.text_detection(image=image)
        
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        return response.text_annotations[1:]

image_detection_api = ImageDetection()