from os import getenv
from io import BytesIO

from google.cloud import vision
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument

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
        
        try:
            response = self.client.text_detection(image=image)

        except GoogleAPICallError as e:
            raise GoogleAPICallError(
                f"API call error: {e.message}\n"
                "For more info on error messages, check: \n"
                "https://cloud.google.com/apis/design/errors"
            )

        except InvalidArgument as e:
            raise InvalidArgument(
                f"Invalid argument: {e.message}\n"
                "For more info on error messages, check: \n"
                "https://cloud.google.com/apis/design/errors"
            )
        
        except Exception as e:
            raise Exception(
                f"Unknown error: {e.message}\n"
                "For more info on error messages, check: \n"
                "https://cloud.google.com/apis/design/errors"
            )

        if response.error.message:
            raise GoogleAPICallError(
                f"{response.error.message}\n"
                "For more info on error messages, check: \n"
                "https://cloud.google.com/apis/design/errors"
            )


        return response.text_annotations[1:]

image_detection_api = ImageDetection()