import requests
import os
import logging

from .database import DatabaseManager
from .r2 import R2_Manager

def send_object(user_id:str, filepath:str, element:str) -> str:
    logging.debug(f"Pass Function: send_object, parameter: user_id: {user_id}, filepath: {filepath}, element: {element}")
    
    try:
        R2_Manager.upload(filepath)
        filepath = os.path.basename(filepath)
        DatabaseManager.update_element(user_id, element, filepath)
        return "ok"
        
    except Exception as e:
        logging.error(f"Error issue occur when send object\n{e}")
        return None