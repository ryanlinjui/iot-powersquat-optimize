import uuid
import os

def create_tmp_filename(extension:str) -> str:
    return f"{str(uuid.uuid4())}.{extension}"

def save_tmp_file(file:bytes, extension:str) -> str:
    tmp_filepath = os.path.join(os.getenv("TEMP_DIRECTORY_PATH"), create_tmp_filename(extension))
    with open(tmp_filepath, "wb") as f:
        f.write(file)
    return tmp_filepath