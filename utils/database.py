'''
Database Information

Table: sensor_uuid_list
    Info: 
        Store the UUIDs of authenticated IoT sensors.

    Column:
        uuid: UUID of IoT sensor.

Table: user
    Info:
        Store temporary data and status for the user.
    
    Column:
        id: User's unique Line ID from Line Server. (It's not that LineID on Line App)
        inbody: Inbody image filepath/URL from cloud storage.
        skeleton: Skeleton video filepath/URL from cloud storage.
        sensor_uuid: User's UUID of IoT sensor.
        sensor_data: The data that IoT sensor collect json filepath/URL from cloud storage.
        analysis_src: Ready for analysis video filepath/URL from cloud storage.
        analysis_result: The video filepath/URL from cloud storage after passing analysis system.
        state: For whole FSM system.
        status: For lock user's event while user's request.
'''

import sqlite3
import os

# Automatically execute the following SQL exection before call any of DatabaseManager's function.
DB_INIT_EXECUTION = [
    "PRAGMA foreign_keys = ON;",
    '''
    CREATE TABLE IF NOT EXISTS sensor_uuid_list (
        uuid TEXT NOT NULL UNIQUE
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS user (
        id TEXT NOT NULL UNIQUE,
        inbody TEXT UNIQUE DEFAULT NULL,
        skeleton TEXT UNIQUE DEFAULT NULL,
        sensor_uuid TEXT UNIQUE DEFAULT NULL,
        sensor_data TEXT UNIQUE DEFAULT NULL,
        analysis_src TEXT UNIQUE DEFAULT NULL,
        analysis_result TEXT UNIQUE DEFAULT NULL,
        state TEXT NOT NULL DEFAULT 'home',
        status BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (sensor_uuid) REFERENCES sensor_uuid_list(uuid),
        CONSTRAINT unique_iot_value UNIQUE (id, inbody),
        CONSTRAINT unique_iot_value UNIQUE (id, skeleton),
        CONSTRAINT unique_iot_value UNIQUE (id, sensor_uuid),
        CONSTRAINT unique_iot_value UNIQUE (id, sensor_data),
        CONSTRAINT unique_iot_value UNIQUE (id, analysis_src),
        CONSTRAINT unique_iot_value UNIQUE (id, analysis_result)
    );
    '''
]

def db_init(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(os.getenv("DATABASE_PATH"), isolation_level=None, check_same_thread=False)
        cursor = conn.cursor()
        for execution in DB_INIT_EXECUTION:
            cursor.execute(execution)
        result = func(conn, cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper

@db_init
def add_sensor_uuid(conn, cursor, uuid:str):
    cursor.execute("INSERT INTO sensor_uuid_list (uuid) VALUES (?)", (uuid,))

class DatabaseManager:
    # mapping variable for dev
    STATE = { 
        "home": "home",
        "inbody": "inbody",
        "iot": "iot",
        "skeleton": "skeleton",
        "analysis": "analysis",
        "return": "return"
    }
    
    @staticmethod
    @db_init
    def insert_user(conn, cursor, user_id:str):
        cursor.execute("INSERT INTO user (id) VALUES (?)", (user_id,))

    @staticmethod
    @db_init
    def delete_user(conn, cursor, user_id:str):
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))

    @staticmethod
    @db_init
    def get_state(conn, cursor, user_id:str) -> str:
        cursor.execute("SELECT state FROM user WHERE id = ?", (user_id,))
        return cursor.fetchone()[0]
    
    @staticmethod
    @db_init
    def get_user_id_by_sensor_uuid(conn, cursor, sensor_uuid:str) -> str:
        cursor.execute("SELECT id FROM user WHERE sensor_uuid = ?", (sensor_uuid,))
        return cursor.fetchone()[0]

    @staticmethod
    @db_init
    def update_state(conn, cursor, user_id:str, state:str):
        if state in DatabaseManager.STATE:
            cursor.execute("UPDATE user SET state = ? WHERE id = ?", (state, user_id,))
    
    @staticmethod
    @db_init
    def get_element(conn, cursor, user_id:str, element:str):
        cursor.execute(f"SELECT {element} FROM user WHERE id = ?", (user_id,))
        return cursor.fetchone()[0]

    @staticmethod
    @db_init
    def update_element(conn, cursor, user_id:str, element:str, value:str):
        cursor.execute(f"UPDATE user SET {element} = ? WHERE id = ?", (value, user_id))
    
    @staticmethod
    @db_init
    def check_element_exist(conn, cursor, user_id:str, element:str) -> bool:
        cursor.execute(f"SELECT {element} FROM user WHERE id = ?", (user_id,))
        result = cursor.fetchone()[0]
        if result:
            return True
        else:
            return False

    @staticmethod
    @db_init
    def reverse_event_status(conn, cursor, user_id:str):
        cursor.execute("UPDATE user SET status = NOT status WHERE id = ?", (user_id,))

    @staticmethod
    @db_init
    def is_user_event_active(conn, cursor, user_id:str) -> bool:
        cursor.execute("SELECT status FROM user WHERE id = ?", (user_id,))
        result = cursor.fetchone()[0]
        if result:
            return bool(result)
        else:
            return False

    @staticmethod
    @db_init
    def get_iot_uuid_list(conn, cursor) -> list:
        cursor.execute("SELECT uuid FROM sensor_uuid_list")
        return [row[0] for row in cursor.fetchall()]

__all__ = ["DatabaseManager"]