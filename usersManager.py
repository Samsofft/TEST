import datetime
import sqlite3

# set
def add(chat_id:int,user_name:str,first_name:str,last_name:str,phone_number:str) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        start_date = str(datetime.datetime.now())
        if not cur.execute(f"SELECT * FROM users WHERE chat_id='{chat_id}'").fetchone():
            cur.execute("INSERT INTO users (chat_id,username,first_name,last_name,phone_number,start_date) VALUES (?,?,?,?,?,?)",
                                        (chat_id,user_name,first_name,last_name,phone_number,start_date,))
            return True
        else: return False

def change_current_keyboard(chat_id:int,keyboard_id:int) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        cur.execute(f"UPDATE users SET current_keyboard_id = '{keyboard_id}' WHERE chat_id='{chat_id}'")
        return True

def change_type(chat_id:int,type:str) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        cur.execute(f"UPDATE users SET account_type = '{type}' WHERE chat_id='{chat_id}'")
        if type == 'paid':
            act_date = str(datetime.datetime.now())
            cur.execute(f"UPDATE users SET act_date = '{act_date}' WHERE chat_id='{chat_id}'")
        return True

def add_music_req(chat_id:int) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        cur.execute(f"UPDATE users SET music_req_count = music_req_count + 1 WHERE chat_id='{chat_id}'")
        print('added')
        return True
    


# get
def get_user_type(chat_id) -> str:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        cur.execute(F"SELECT account_type FROM users WHERE chat_id='{chat_id}'")
        type = cur.fetchone()
        if not type:
            return None
        else:
            return type[0]

def get_current_keyboard_id(chat_id:int) -> int:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        keyboard_id = cur.execute(f"SELECT current_keyboard_id  FROM users WHERE chat_id='{chat_id}'").fetchone()
        if not keyboard_id:
            return None
        else:
            return int(keyboard_id[0])

def get_id_by_name(name:str) -> int:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        user_id = cur.execute(f"SELECT chat_id FROM users WHERE first_name || ' ' || last_name LIKE '%{name}%'").fetchone()
        if not user_id:
            return None
        else:
            return user_id[0]

def admins_id_list() -> list:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        admins_id = cur.execute(f"SELECT chat_id FROM users WHERE account_type='admin'").fetchall()
        admins_id_list = [id[0] for id in admins_id]
        return admins_id_list

def paid_users_count() -> int:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        active_users_count = cur.execute(f"SELECT count(*) FROM users WHERE account_type='paid'").fetchone()
        return active_users_count[0]
    
def demo_users_count() -> int:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        active_users_count = cur.execute(f"SELECT count(*) FROM users WHERE account_type='demo'").fetchone()
        return active_users_count[0]
    
def music_req_count(chat_id:int) -> int:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        music_req_count = cur.execute(f"SELECT music_req_count  FROM users WHERE chat_id='{chat_id}'").fetchone()
        if not music_req_count[0]:
            print(0)
            return 0
        else:
            print(music_req_count[0])
            return music_req_count[0] 