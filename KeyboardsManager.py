import sqlite3
from pyrogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup


def add_button_with_reply_keyboard(keyboard_id:int,button_name:str) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor() 
        if not cur.execute(f"SELECT id FROM buttons WHERE name = '{button_name}' AND keyboard_id = '{keyboard_id}'").fetchall():
            cur.execute(f"INSERT INTO keyboards (name,previous_keyboard_id,type) VALUES ('{button_name}',{keyboard_id},'reply')")
            cur.execute(f"SELECT id FROM keyboards WHERE name = '{button_name}' AND previous_keyboard_id = '{keyboard_id}'")
            button_data = cur.fetchone()
            cur.execute(f"INSERT INTO buttons(name,keyboard_id,type,data) VALUES ('{button_name}','{keyboard_id}','keyboard','{button_data[0]}')")
            return True
        else: return False
    
def add_button_with_inline_keyboard(keyboard_id:str,button_name:str) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor() 
        if not cur.execute(f"SELECT id FROM buttons WHERE name = '{button_name}' AND keyboard_id = '{keyboard_id}'").fetchall():
            cur.execute(f"INSERT INTO keyboards (name,previous_keyboard_id,type) VALUES ('{button_name}',{keyboard_id},'inline')")
            cur.execute(f"SELECT id FROM keyboards WHERE name = '{button_name}' AND previous_keyboard_id = '{keyboard_id}'")
            button_data = cur.fetchone()
            cur.execute(f"INSERT INTO buttons(name,keyboard_id,type,data) VALUES ('{button_name}','{keyboard_id}','keyboard','{button_data[0]}')")
            return True
        else: return False

def add_button_with_file(keyboard_id:int,button_name:str,file_id:str,notes:str,type:str) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor() 
        if not cur.execute(f"SELECT id FROM buttons WHERE name = '{button_name}' AND keyboard_id = '{keyboard_id}'").fetchall():
            cur.execute(f"INSERT INTO buttons(name,keyboard_id,type,data,notes) VALUES ('{button_name}','{keyboard_id}','{type}','{file_id}','{notes}')")
            return True
        else: return False

def add_button_with_url(keyboard_id:int,button_name:str,url:str) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor() 
        if not cur.execute(f"SELECT id FROM buttons WHERE name = '{button_name}' AND keyboard_id = '{keyboard_id}'").fetchall():
            cur.execute(f"INSERT INTO buttons(name,keyboard_id,type,data) VALUES ('{button_name}','{keyboard_id}','url','{url}')")
            return True
        else: return False 

def get_button_data_from_name(keyboard_id:int,button_name:str) -> int:
    if button_name == 'رجوع':
        with sqlite3.connect('garage.db') as db: 
            cursor = db.cursor()
            cursor.execute(f'SELECT previous_keyboard_id FROM keyboards WHERE id = {keyboard_id}')
            previous_keyboard_id = cursor.fetchone()
            return int(previous_keyboard_id[0])
    else:
        with sqlite3.connect('garage.db') as db:
            cursor = db.cursor()
            button_data = cursor.execute(f"SELECT data FROM buttons WHERE name= '{button_name}' AND keyboard_id = {keyboard_id}").fetchone()
            try:
                if not button_data[0]:
                    return None
                else:
                    return int(button_data[0])
            except:
                print('error with keyboard (connection error posible)')
            

def get_button_from_id(button_id:str):
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor() 
        button = cur.execute(f"SELECT name,type,data,notes FROM buttons WHERE id = '{button_id}'").fetchone()
        return button

def get_keyboard_type(keyboard_id:int) -> str:
    with sqlite3.connect('garage.db') as db:
        cursor = db.cursor()
        type = cursor.execute(f'SELECT type FROM keyboards WHERE id = {keyboard_id}').fetchone()
        return type[0]
    
def get_keyboard_markup(keyboard_id:int):
    with sqlite3.connect('garage.db') as db:
        cursor = db.cursor()
        keyboard = cursor.execute(f'SELECT raws,type FROM keyboards WHERE id = {keyboard_id}').fetchone()
        if not keyboard:
            return None
        else:
            raws,type = keyboard[0],keyboard[1]
            cursor.execute(f'SELECT id,name,type,data FROM buttons WHERE keyboard_id = {keyboard_id}')
            buttons = cursor.fetchall()
            if type == 'reply':
                return reply_markup(raws,buttons,keyboard_id)
            else:
                return inline_markup(raws,buttons)

def get_band_for_video(keyboard_id:int):
    with sqlite3.connect('garage.db') as db:
        cursor = db.cursor()
        previous_keyboard_id = cursor.execute(f'SELECT previous_keyboard_id FROM keyboards WHERE id = {keyboard_id}').fetchone()
        previous_keyboard_id = previous_keyboard_id[0]
        band = cursor.execute(f'SELECT name FROM keyboards WHERE id = {previous_keyboard_id}').fetchone()
        return band[0]

def search_audio(text:str):
    with sqlite3.connect('garage.db') as db:
        cursor = db.cursor()
        data = cursor.execute(f"SELECT id,name,type,data,notes FROM buttons WHERE name LIKE '%{text}%' AND type = 'audio'").fetchall()
        return data
    
def search_video(text:str):
    with sqlite3.connect('garage.db') as db:
        cursor = db.cursor()
        data = cursor.execute(f"SELECT id,name,type,data,notes FROM buttons WHERE name LIKE '%{text}%' AND type = 'video'").fetchall()
        return data
    
def del_button(keyboard_id:int,button_name:str) -> bool:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor() 
        data = cur.execute(f"SELECT id,type,data FROM buttons WHERE name = '{button_name}' AND keyboard_id = '{keyboard_id}'").fetchone()
        if not data:
            print(f"button {button_name} not found")
            return False
        else:
            button_id,type,data = data[0],data[1],data[2]
            print(f"button {button_name}, id {button_id}, type {type},data {data} found, deleting...")
            if type == 'keyboard':
                keyboard_buttons = cur.execute(f"SELECT name FROM buttons WHERE keyboard_id = '{data}'").fetchall()
                keyboard_buttons_names = [button[0] for button in keyboard_buttons]
                cur.execute(f"DELETE FROM buttons WHERE id = '{button_id}' AND keyboard_id = '{keyboard_id}'")
                cur.close()
                db.commit()
                for name in keyboard_buttons_names:
                    del_button(data,name)
            else:
                cur.execute(f"DELETE FROM buttons WHERE id = '{button_id}' AND keyboard_id = '{keyboard_id}'")
            cur = db.cursor()
            cur.execute(f"DELETE FROM keyboards WHERE id = '{data}'")
            print(f"keyboard {data} deleted")
            return True
            
def edit_keyboard_raws(keyboard_id:int,raws:int):
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        cur.execute(f"UPDATE keyboards SET raws = {raws} WHERE id = {keyboard_id}")

def get_keyboard_buttons_count(keyboard_id:int) -> int:
    with sqlite3.connect('garage.db') as db:
        cur = db.cursor()
        count = cur.execute(f"SELECT COUNT(*) FROM buttons WHERE keyboard_id = {keyboard_id}").fetchone()
        return count[0]
        
def inline_markup(raws:int,buttons:list) -> InlineKeyboardMarkup:
        inline_buttons = []
        for button in buttons:
            if button[2] == 'url':
                inline_button = InlineKeyboardButton(button[1],url=str(button[3]))
            else: 
                inline_button = InlineKeyboardButton(button[1],str(button[0]))
            inline_buttons.append(inline_button)
        if len(inline_buttons) <= 93:
            buttons_in_rows = [inline_buttons[i:i + raws] for i in range(0, len(inline_buttons), raws)]
            buttons_in_rows.append([InlineKeyboardButton('حذف القائمة','Delete')])
            inline_keyboard = InlineKeyboardMarkup( buttons_in_rows)
            return inline_keyboard
        else:
            buttons_in_rows = [inline_buttons[i:i + raws] for i in range(0, 93, raws)]
            buttons_in_rows.append([InlineKeyboardButton('حذف القائمة','Delete')])
            buttons_in_rows2 = [inline_buttons[i:i + raws] for i in range(93, len(inline_buttons), raws)]
            buttons_in_rows2.append([InlineKeyboardButton('حذف القائمة','Delete')])
            inline_keyboard = InlineKeyboardMarkup( buttons_in_rows)
            inline_keyboard2 = InlineKeyboardMarkup( buttons_in_rows2)
            return [inline_keyboard,inline_keyboard2]
    
def reply_markup(raws:int,buttons:list,Keyboard_id:int) -> ReplyKeyboardMarkup:
        reply_buttons = []
        for button in buttons:
            reply_buttons.append(KeyboardButton(button[1]))
        buttons_in_rows = [reply_buttons[i:i + raws] for i in range(0, len(reply_buttons), raws)]
        if Keyboard_id > 1:
            buttons_in_rows.insert(0,[KeyboardButton('رجوع')])
        reply_keyboard = ReplyKeyboardMarkup(keyboard= buttons_in_rows,resize_keyboard=True)
        return reply_keyboard

