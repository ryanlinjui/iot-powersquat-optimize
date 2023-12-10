'''
Database Information

Table: iot_uuid
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
        iot: The data that IoT sensor collect json filepath/URL from cloud storage.
        analysis: Ready for analysis video filepath/URL from cloud storage.
        state: For whole FSM system.
        status: For lock user's event while user's request.
'''

import sqlite3
import os

# Automatically execute the following SQL exection before call any of DatabaseManager's function.
DB_INIT_EXECUTION = [
    "PRAGMA foreign_keys = ON;",
    '''
    CREATE TABLE IF NOT EXISTS iot_uuid (
        uuid TEXT NOT NULL UNIQUE
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS user (
        id TEXT NOT NULL UNIQUE,
        inbody TEXT UNIQUE DEFAULT NULL,
        skeleton TEXT UNIQUE DEFAULT NULL,
        iot TEXT DEFAULT NULL,
        analysis TEXT UNIQUE DEFAULT NULL,
        state TEXT NOT NULL DEFAULT 'home',
        status BOOLEAN NOT NULL DEFAULT FALSE,
        FOREIGN KEY (iot) REFERENCES iot_uuid(uuid),
        CONSTRAINT unique_iot_value UNIQUE (id, iot)
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
def add_iot_uuid(conn, cursor, uuid:str):
    cursor.execute("INSERT INTO iot_uuid (uuid) VALUES (?)", (uuid,))

class DatabaseManager:
    # mapping variable for dev
    STATE = { 
        "home": "home",
        "inbody": "inbody",
        "skeleton": "skeleton",
        "iot":  "iot",
        "analysis": "analysis",
        "return": "return"
    }
    
    @db_init
    def insert_user(conn, cursor, user_id:str):
        cursor.execute("INSERT INTO user (id) VALUES (?)", (user_id,))

    @db_init
    def delete_user(conn, cursor, user_id:str):
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))

    @db_init
    def get_state(conn, cursor, user_id:str) -> int:
        cursor.execute("SELECT state FROM user WHERE id = ?", (user_id,))
        return cursor.fetchone()[0]

    @db_init
    def update_state(conn, cursor, user_id:str, state:str):
        if state in DatabaseManager.STATE:
            cursor.execute("UPDATE user SET state = ? WHERE id = ?", (state, user_id,))

    @db_init
    def update_element(conn, cursor, user_id:str, element:str, value:str):
        cursor.execute(f"UPDATE user SET {element} = ? WHERE id = ?", (value, user_id))
    
    @db_init
    def check_element_exist(conn, cursor, user_id:str, element:str) -> bool:
        cursor.execute(f"SELECT {element} FROM user WHERE id = ?", (user_id,))
        result = cursor.fetchone()[0]
        if result:
            return True
        else:
            return False

    @db_init
    def reverse_event_status(conn, cursor, user_id:str):
        cursor.execute("UPDATE user SET status = NOT status WHERE id = ?", (user_id,))

    @db_init
    def is_user_event_active(conn, cursor, user_id:str) -> bool:
        cursor.execute("SELECT status FROM user WHERE id = ?", (user_id,))
        result = cursor.fetchone()[0]
        if result:
            return bool(result)
        else:
            return False

    @db_init
    def get_iot_uuid_list(conn, cursor) -> list:
        cursor.execute("SELECT uuid FROM iot_uuid")
        return [row[0] for row in cursor.fetchall()]

__all__ = ["DatabaseManager"]

if __name__ == "__main__":
    DatabaseManager.add_iot_uuid("1bc68b2a")
    # DatabaseManager.insert_user("test")
    # DatabaseManager.update_element("test", "iot","123")