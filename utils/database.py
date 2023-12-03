import sqlite3

COL = [
    "home",
    "inbody",
    "skeleton",
    "analysis",
    "iot",
    "return"
]

STATE = {
    COL[0]: 0,
    COL[1]: 1,
    COL[2]: 2,
    COL[3]: 3,
    COL[4]: 4,
    COL[5]: 5
}

# TODO block user action for each menu case when user thread is running

DB_INIT_EXECUTION = '''
    CREATE TABLE IF NOT EXISTS user (
        id TEXT NOT NULL UNIQUE,
        inbody TEXT DEFAULT NULL,
        skeleton TEXT DEFAULT NULL,
        iot TEXT DEFAULT NULL,
        analysis TEXT DEFAULT NULL,
        state INTEGER NOT NULL DEFAULT 0
    )
'''

DB_FILEPATH = "./database/user.db"

class DatabaseManager:
    def db_init(func):
        def wrapper(*args, **kwargs):
            conn = sqlite3.connect(DB_FILEPATH, isolation_level=None, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(DB_INIT_EXECUTION)
            result = func(conn, cursor, *args, **kwargs)
            conn.commit()
            conn.close()
            return result
        return wrapper

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
    def update_state(conn, cursor, user_id:str, state_num:int):
        if state_num < 0 or state_num > 4: return
        cursor.execute("UPDATE user SET state = ? WHERE id = ?", (state_num, user_id,))

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

if __name__ == "__main__":
    DatabaseManager.delete_user("test")
    DatabaseManager.insert_user("test")