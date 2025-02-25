import telebot
from  telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiException
import sqlite3
from start_button import API_key, send_welcome, handle_start_button


bot = telebot.TeleBot(API_key)

bmd = "CAACAgIAAxkBAAIBlmdxZi6sK42VCA3-ogaIn30MXGrmAAJnIAACKVtpSNxijIXcPOrMNgQ"

holatbot = True


def setup_database_followers():
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS followers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_name TEXT,
            channel_url TEXT,
            num_follower INTEGER,
            now_follower INTEGER

        )
    ''')
    conn.commit()
    conn.close()

def setup_block_user():
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blockers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number_blok INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# def bir():
#     conn = sqlite3.connect("bot_file.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#             INSERT INTO blockers (number_blok)
#             VALUES (?)
#         ''', (0,))
#     conn.commit()
# bir()


def setup_database_file():
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_kod INTEGER,
            file_id TEXT,
            file_name TEXT,
            file_type TEXT

        )
    ''')
    conn.commit()
    conn.close()

def save_file(file_kod, file_id, file_name,file_type):
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO files (file_kod, file_id, file_name, file_type)
        VALUES (?, ?, ?,?)
    ''', (file_kod, file_id, file_name,file_type))
    conn.commit()
    conn.close()

# Get file metadata from the database
def get_file(file_kod):
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_id, file_name, file_type FROM files WHERE file_kod = ?', (file_kod,))
    file = cursor.fetchall()
    conn.close()
    return file

def get_ani_kod(name):
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_kod,file_name  FROM files')
    fil = cursor.fetchall()
    l_a = []
    for x in fil:
        if name in x[1].lower() and x not in l_a:
            l_a.append(x)
    if len(l_a) == 0:
        l_a = [("Natija", "topilmadi.")]
    return l_a

def get_last_kod():
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_kod  FROM files')
    kod = max(cursor.fetchall())
    return kod

def show_anime_list():
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_kod, file_name  FROM files')
    names = cursor.fetchall()
    ls = ["Animelar Ro'yhati"]
    lr = []
    for x in names:
        if x not in lr:
            lr.append(x)
            ls.append(f"{x[0]}:  {x[1]}\n")
    return ls


def setup_database():
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        join_date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def setup_admin():
    conn = sqlite3.connect("bot_file.db",check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        join_date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def log_admin(user_id, username, first_name, last_name):
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO admins (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        """, (user_id, username, first_name, last_name))
        conn.commit()

    except sqlite3.Error as e:
        print("Error logging admin:", e)
    finally:
        conn.close()




# Count total users
def count_users():
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count








#Keyboards-------------------------

def get_control_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_st = types.KeyboardButton('📊Statistika')
    item_xy = types.KeyboardButton("📃Xabar yuborish")
    item_pt = types.KeyboardButton("📬Post tayyorlash")
    item_as = types.KeyboardButton("🎥Anime sozlash")
    item_kl = types.KeyboardButton("📢Kanallar")
    item_ad = types.KeyboardButton("📋Adminlar")
    item_bh = types.KeyboardButton("🤖Bot holati")
    item_bc = types.KeyboardButton("◀️Orqaga")

    markup.row(item_st, item_xy)
    markup.row(item_pt,item_as, item_kl)
    markup.row(item_ad, item_bh)
    markup.row(item_bc)
    return markup

def main_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin(message.chat.id):
        item_BH = types.KeyboardButton(text="🛂Boshqaruv")
        markup.row(item_BH)
    return markup






def is_admin(user_id):
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins")
    ids_of_admin = cursor.fetchall()
    for x in ids_of_admin:
        if user_id == x[1]:
            return True
    return False



# checking Inchannel----------------------------
channel_id = "@telegrabotkrito"

def check_user_in_channel(message):
    if message.chat.type in ["group", "supergroup"]:
        return True
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM followers")
    ll = cursor.fetchall()

    for i in ll:
        try:
            s:str = i[2]
            url1: str = f"@{s[13:]}"
            member = bot.get_chat_member(chat_id= url1, user_id = message.chat.id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            print(f"channel_Error: {e}")
            return False
    return True


    



# Starts bot--------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: call.data == "send_start")
def a2(call):
    handle_start_button(call)
    send_welcome(call.message)

@bot.message_handler(commands = ['start'])
def a1(message):
    if message.chat.type in ["group", "supergroup"]:
        return
    send_welcome(message)




#Boshqaruv paneli----------------

broadcast_mode = False
@bot.message_handler(func= lambda message: message.text == "🛂Boshqaruv")
def control(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "✅Siz admin ekanligingiz tasdiqlandi.",reply_markup= get_control_keyboard())
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAICmWd2qLc5grUQzAkIASgXwR4-jW1FAAKfGgAC43BwSQoc1Niaab0fNgQ")
    else:
        bot.send_message(message.chat.id, "❌Siz bu tizimdan foyadalanish huquqiga ega emasiz.")
        bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAICk2d2pwlY_Az7yUl1HN1qkEGGlkLmAAI2EwACGJ3wUKir7ygymVAENgQ")



#statistika tugmasi----------------------------
def blockers_pp():
    s = 0
    conn = sqlite3.connect("bot_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    peaple = cursor.fetchall()
    for user_id in peaple:
        try:
            bot.send_message(chat_id=user_id[1], text="Hello! Just testing 😊")
        except ApiException as e:
            if "Forbidden: bot was blocked by the user" in str(e):
                s += 1


    cursor.execute("UPDATE blockers SET number_blok = ? WHERE id = ?", (s, 1))
    conn.commit()
    cursor.execute("SELECT * FROM blockers")
    try:
        return cursor.fetchone()
    except:
        return 0

@bot.callback_query_handler(func= lambda call: call.data == "num_blockers")
def num_b(call):
    son = blockers_pp()
    if son == None:
        son = 0
    bot.send_message(call.message.chat.id, f"❇️Faol foydalanuvchilar soni: {count_users() - int(son)}\n⭕️Blocklagan boydalanuvchilar soni: {son} " )

def bl_keybord():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Blocklagan foydalanuvchilar soni", callback_data="num_blockers")
    keyboard.add(button)
    return keyboard


@bot.message_handler(func= lambda message: message.text == "📊Statistika" and is_admin(message.chat.id))
def user_num(message):
    bot.send_message(message.chat.id, f"📋Bot foydalanuvchilar soni: {count_users()}" ,reply_markup= bl_keybord())



#Broadcast tugmasi-----------------------------

@bot.message_handler(func= lambda message: message.text == "📃Xabar yuborish" and is_admin(message.chat.id))
def start_broadcast(message):
    global broadcast_mode
    if is_admin(message.chat.id):
        broadcast_mode = True
        bot.send_message(message.chat.id, text= "❇️Yuboriladigan xabarni yozing...")
    else:
        bot.send_message(message.chat.id, "❌Siz bu tizimdan foyadalanish huquqiga ega emasiz.")
        bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAICk2d2pwlY_Az7yUl1HN1qkEGGlkLmAAI2EwACGJ3wUKir7ygymVAENgQ")







#🎥Anime sozlash--------------------------------------------------------------------------------------------------
get_anime = False
get_anime_nom = False
anime_del = False
anime_change = False
anime_kod = get_last_kod()[0]
file_n: str = ""
file_list = []

@bot.message_handler(func = lambda message: message.text == "🎥Anime sozlash" and is_admin(message.chat.id))
def create_keyboard_of_anime_change(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_st = types.KeyboardButton("❇️Anime qo'shish")
    item_xy = types.KeyboardButton("🗑Anime o'chrish")
    item_pt = types.KeyboardButton("🔱O'zgartirish")
    item_ls = types.KeyboardButton("📃Anime ro'yhati")
    item_bc = types.KeyboardButton("◀️Orqaga")

    markup.row(item_st, item_xy)
    markup.row(item_pt,item_ls)
    markup.row(item_bc)

    bot.send_message(message.chat.id, "Anime Sozlash bo'limi!", reply_markup= markup)

@bot.message_handler(func = lambda message: message.text == "❇️Anime qo'shish" and is_admin(message.chat.id))
def add_anime(message):
    global get_anime_nom, anime_kod
    get_anime_nom = True
    anime_kod += 1
    bot.send_message(message.chat.id , "📃Ok, yuklamoqchi bo'lgan animening nomini tashlang...")

@bot.message_handler(func = lambda message: get_anime_nom and is_admin(message.chat.id))
def get_file_name(message):
    global file_n, get_anime, get_anime_nom
    file_n = message.text
    get_anime = True
    get_anime_nom = False
    bot.send_message(message.chat.id , "🖼Ok, yuklamoqchi bo'lgan animening suratini tashlang.")


@bot.message_handler(content_types=['photo', 'video'], func = lambda message: get_anime and is_admin(message.chat.id))
def handle_file_upload(message):
    global anime_kod, file_n
    file_id = None
    if message.photo:
        file_id = message.photo[-1].file_id  # Get the largest photo
        file_type = 'photo'
        bot.send_message(message.chat.id, "🎥Ok, yuklamoqchi bo'lgan anime qismlarini tartib bo'yicha tashlang (1 -> 12)")
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
    else:
        bot.reply_to(message, "⛔️Unsupported file type.")
        return

    # Save file metadata to database
    #save_file(anime_kod, file_id, file_n,file_type)
    if file_id:
        file_list.append({"message_id": message.message_id, "file_id": file_id, "file_type": file_type})
        file_list.sort(key=lambda x: x["message_id"])
        
    bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")

@bot.message_handler(func = lambda message: is_admin(message.chat.id), commands= ["save"])
def finish_file_upload(message):
    global anime_kod, file_n, file_list
    sorted_files = file_list
    for file in sorted_files:
        save_file(anime_kod, file["file_id"], file_n, file["file_type"])
    bot.reply_to(message, f"✅{file_n.capitalize()} saved successfully!")
    file_list = []




@bot.message_handler(func= lambda message: message.text == "🗑Anime o'chrish" and is_admin(message.chat.id))
def del_anime(message):
    global anime_del
    anime_del = True
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += (i + "\n")
    bot.send_message(message.chat.id, m)
    bot.send_message(message.chat.id, "O'chirmoqchi bo'lgan anime kodini kiriting...")

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and anime_del)
def delete_anime_from_anime_list(message):
    global anime_del
    anime_del = False
    try:
        kod = int(message.text)
        conn = sqlite3.connect("bot_file.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM files WHERE file_kod = ?", (kod,))
        conn.commit()
        bot.send_message(message.chat.id, "✅Anime muvaffaqiyatli o'chirildi")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik yuz berdi: {e}")


add_ep_bool1 = False
add_ep_bool2 = False
ep_num: int = 0
an_name: str = "Unknown"


@bot.callback_query_handler(func= lambda call: call.data == "ep_anime")
def change_anime_ep(call):
    global add_ep_bool1
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += (i + "\n")
    bot.send_message(call.message.chat.id, m)
    bot.send_message(call.message.chat.id, "Qism qo'shiladigan anime kodini kiriting...")
    add_ep_bool1 = True

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and add_ep_bool1)
def add_episode(message):
    global ep_num, an_name, add_ep_bool1, add_ep_bool2
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_kod, file_name FROM files")
    eplist = cursor.fetchall()
    for i in eplist:
        if int(i[0]) == int(message.text):
            an_name = i[1]
            break
    if an_name == "Unknown":
        bot.send_message(message.chat.id,"Siz mavjud bo'lmagan kod kiritingiz!")
    else:
        ep_num = message.text
        add_ep_bool2 = True
        bot.send_message(message.chat.id, f"🎥Ok, {an_name} animesiga yuklamoqchi bo'lgan qismni/larni tartib bo'yicha tashlang...")
    add_ep_bool1 = False

@bot.message_handler(content_types=['video'], func = lambda message: add_ep_bool2 and is_admin(message.chat.id))
def handle_file_upload(message):
    global ep_num,an_name
    if message.video:
        file_id = message.video.file_id
        file_type = 'video'
    else:
        bot.reply_to(message, "⛔️Unsupported file type.")
        return

    # Save file metadata to database
    save_file(ep_num, file_id, an_name,file_type)

    bot.reply_to(message, f"✅{file_type.capitalize()} saved successfully!")




@bot.callback_query_handler(func= lambda call: call.data == "name_anime")
def change_anime_name(call):
    global anime_change
    anime_change = True
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += (i + "\n")
    bot.send_message(call.message.chat.id, m)
    bot.send_message(call.message.chat.id, "O'zgartirmoqchi bo'lgan anime kodi va yangi nomini kiriting Eg. 1, Anime_name. Vergul bo'lishi shart.")


@bot.message_handler(func= lambda message: anime_change and is_admin(message.chat.id))
def change_name(message):
    global anime_change
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    k = message.text.split(",")
    try:
        cursor.execute("UPDATE files SET file_name = ? WHERE file_kod = ?", (k[1], int(k[0])))
        conn.commit()
        bot.send_message(message.chat.id, "✅Anime muvaffaqiyatli o'zgartirildi.")

    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik yuz berdi: {e}")
    finally:
        anime_change = False


@bot.message_handler(func=lambda message: message.text == "🔱O'zgartirish" and is_admin(message.chat.id))
def change_anime(message):
    keyboard = InlineKeyboardMarkup()
    button_name = InlineKeyboardButton(text="Nomini o'zgartish", callback_data= "name_anime")
    button_ep = InlineKeyboardButton(text="Qismini o'zgartirish", callback_data= "ep_anime")
    keyboard.add(button_ep,button_name)
    bot.send_message(message.chat.id, "Animeni qanday o'zgartirmoqchisiz ?", reply_markup=keyboard)


@bot.message_handler(func= lambda message: message.text == "📃Anime ro'yhati" and is_admin(message.chat.id))
def list_anime(message):
    roy = show_anime_list()
    m = ""
    for i in roy:
        m += (i + "\n")
    bot.send_message(message.chat.id, m)





#📬Post tayyorlash----------------------------------------------------------------------------------------------------------------
kd_bool = False
kd = 0
get_post_bool = False

@bot.message_handler(func = lambda message: message.text == "📬Post tayyorlash" and is_admin(message.chat.id))
def create_post(message):
    global kd_bool
    kd_bool = True
    bot.send_message(message.chat.id, "Iltimos, Anime ko'dini kiriting.")

@bot.message_handler(func= lambda message: is_admin(message.chat.id) and kd_bool)
def get_post(message):
    global kd, kd_bool, get_post_bool
    kd_bool = False
    get_post_bool = True
    kd = int(message.text)
    bot.send_message(message.chat.id, "Iltimos, foto va anime postingizni tashlang...")

@bot.message_handler(content_types= ["text", "photo"] ,func= lambda message: is_admin(message.chat.id) and get_post_bool)
def ready_post(message):
    global kd
    link = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text ="🔹👉Anime ko'rish" ,url = f"https://t.me/insta_animelar_bot?start={kd}")
    link.add(button)
    if message.content_type == "photo":
        bot.send_photo(message.chat.id, message.photo[-1].file_id, caption=message.caption, reply_markup= link)
    else:
        bot.send_message(message.chat.id, "Siz noto'g'ri turdagi xabar yubordiz!")




#"📢Kanallar"-----------------------------------------
add_channel_bool = False
del_channel_bool = False

@bot.callback_query_handler(func= lambda call: call.data == "add_channel")
def channel_add_to_list(call):
    global add_channel_bool
    add_channel_bool = True
    bot.send_message(call.message.chat.id, "Kanal nomini, silkasisini va qo'shiluvchilar soni  vergul bilan ajratib kiriting .\nkanal_nomi,kanal_silkasi,100")


@bot.callback_query_handler(func= lambda call: call.data == "del_channel")
def channel_add_to_list(call):
    global del_channel_bool
    del_channel_bool = True
    bot.send_message(call.message.chat.id, "Kanal kodini kiriting.")

@bot.message_handler(func = lambda message: message.text == "📢Kanallar" and is_admin(message.chat.id))
def channel_list(message):
    keyboard = InlineKeyboardMarkup()
    button_add = InlineKeyboardButton(text="➕Kanal qo'shish", callback_data="add_channel")
    button_del = InlineKeyboardButton(text="➖Kanal o'chrish", callback_data="del_channel")
    keyboard.add(button_add)
    keyboard.add(button_del)
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM followers")
    ch_list = cursor.fetchall()
    mm: str = ""
    for c in ch_list:
        mm += f"{c[0]}. {c[1]} , {c[2]} , {c[4]}\n"
    try:
        bot.send_message(message.chat.id, mm, reply_markup= keyboard)
    except:
        bot.send_message(message.chat.id, "Kanal qo'sh !", reply_markup= keyboard)



@bot.message_handler(func= lambda message: is_admin(message.chat.id) and add_channel_bool)
def addchannel(message):
    global add_channel_bool
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()

    m = message.text.split(",")
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO followers (channel_name,channel_url, num_follower, now_follower)
        VALUES (?, ?, ?,?)
        """, (m[0],m[1],m[2],0))
        conn.commit()

        bot.send_message(message.chat.id, "✅Kanal muvoffaqiyatli qo'shildi.")
    except sqlite3.Error as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
    finally:
        add_channel_bool = False
        conn.close()



@bot.message_handler(func= lambda message: is_admin(message.chat.id) and del_channel_bool)
def delchannel(message):
    global del_channel_bool
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM followers WHERE id = ?", (int(message.text),))
        conn.commit()

        bot.send_message(message.chat.id, "✅Kanal muvoffaqiyatli o'chirildi")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
    finally:
        del_channel_bool = False




#Admins tugmasi--------------------------------------
enable_add = False
enable_del = False
def send_demand1(message):
    bot.send_message(message.chat.id, "📃Admin qilmoqchi bo'lgan shaxsning 'username'ini  kiriting...")
def send_demand2(message):
    bot.send_message(message.chat.id, "🔢Admin raqamini jo'nating...")
@bot.callback_query_handler(func= lambda call: call.data == "add_admin")
def admin_add(call):
    global enable_add, enable_del
    enable_add = True
    enable_del = False
    send_demand1(call.message)

@bot.callback_query_handler(func= lambda call: call.data == "del_admin")
def admin_del(call):
    global enable_del, enable_add
    enable_del = True
    enable_add = False
    send_demand2(call.message)



@bot.message_handler( func= lambda message: message.text == "📋Adminlar" and is_admin(message.chat.id))
def show_admins(message):
    keyboard = InlineKeyboardMarkup()
    button_add = InlineKeyboardButton(text="➕Admin qo'shish", callback_data= "add_admin")
    button_del = InlineKeyboardButton(text="➖Admin o'chrish", callback_data= "del_admin")
    keyboard.add(button_add)
    keyboard.add(button_del)
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM admins""")
    adminlar = cursor.fetchall()
    mes_to_admin: str = ""
    for person in adminlar:

        mes_to_admin += f"{person[0]}."
        if person[2] != None:
            mes_to_admin += f" {person[2]},"
        if person[3] != None:
            mes_to_admin += f" {person[3]},"
        if person[4] != None:
            mes_to_admin += f" {person[4]},"
        mes_to_admin += "\n"

    try:
        bot.send_message(message.chat.id, mes_to_admin, reply_markup= keyboard)
    except:
        bot.send_message(message.chat.id, "Admin qo'sh !", reply_markup= keyboard)



@bot.message_handler(func= lambda message: is_admin(message.chat.id) and enable_add)
def search_admin(message):
    global enable_add

    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users""")
    people = cursor.fetchall()
    try:
        num = int(message.text)
        for p in people:
            if p[0] == num:

                log_admin(p[1],p[2],p[3],p[4])
                bot.send_message(message.chat.id, "✅Yangi Admin o'rnatildi")
                break

        enable_add = False

    except ValueError:
        mes_to_admin: str = ""
        for person in people:

            if message.text in person:
                mes_to_admin += f"{person[0]}."
                if person[2] != None:
                    mes_to_admin += f" {person[2]},"
                if person[3] != None:
                    mes_to_admin += f" {person[3]},"
                if person[4] != None:
                    mes_to_admin += f" {person[4]},"
                mes_to_admin += "\n"
        bot.send_message(message.chat.id, f"Natijalar:\n{mes_to_admin}Ism oldidagi raqamni jo'nating")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
        enable_add = False


@bot.message_handler(func=lambda message: is_admin(message.chat.id) and enable_del)
def search_admin(message):
    global enable_del

    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM admins""")
    try:
        num = int(message.text)
        cursor.execute("DELETE FROM admins WHERE id = ?", (num,))
        conn.commit()
        enable_del = False
        bot.send_message(message.chat.id, "😎Adim muvoffaqiyatli o'chirildi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔️Tizimda xatolik: {e}")
        enable_del = False


#bot holati tugmasi----------------------------------
@bot.callback_query_handler(func= lambda call: call.data == "starts")
def startsbot(call):
    global holatbot
    holatbot = True
    switch(call.message)

def startbot(message):
    mes_key = InlineKeyboardMarkup()
    but1 = InlineKeyboardButton(text= "✅Turn On" , callback_data= "starts")
    mes_key.add(but1)
    bot.send_message(message.chat.id, "⛔️Bot to'xtatildi.", reply_markup= mes_key)


@bot.callback_query_handler(func= lambda call: call.data == "stop")
def stops(call):
    global holatbot
    holatbot = False
    startbot(call.message)

@bot.message_handler(func = lambda message: message.text == "🤖Bot holati" and is_admin(message.chat.id))
def switch(message):
    global holatbot
    if is_admin(message.chat.id):
        keyboard = InlineKeyboardMarkup()
        if holatbot:
            hol = "Ishalamoqda"
        else:
            hol = "To'xtatilgan"
        button2 = InlineKeyboardButton(text="🚷Turn off", callback_data="stop")

        keyboard.add(button2)
        bot.send_message(message.chat.id, f"😇Bot holati: {hol}", reply_markup= keyboard )



#Back tugmasi---------------------------------------------
@bot.message_handler(func= lambda message: message.text == "◀️Orqaga")
def back(message):
    if message.chat.type in ["group", "supergroup"]:
        return
    global get_anime, get_anime_nom,anime_del, anime_change
    get_anime = False
    get_anime_nom = False
    anime_del = False
    anime_change = False
    bot.send_message(message.chat.id, "📋Bosh menyu", reply_markup= main_keyboard(message))



#Anime Izlash
@bot.message_handler(content_types=["text", "photo", "video", "audio", "document","sticker"], func= lambda message: holatbot )
def kod_check(message):
    global anime_kod, broadcast_mode
    mmm = message.text
    if message.chat.type in ["group", "supergroup"] and "kkk" not in message.text:
        return
    else:
        mmm = message.text[4:]

    
    if is_admin(message.chat.id) and broadcast_mode:
        conn = sqlite3.connect("bot_file.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        peaple = cursor.fetchall()
        for user in peaple:

            try:
                user_id = user[1]
                if int(user_id) == 7651554989:
                    print("bo'timiz")
                elif message.content_type == "text":
                    bot.send_message(user_id, message.text)
                    # Broadcast photos
                elif message.content_type == "photo":
                    bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
                    # Broadcast videos
                elif message.content_type == "video":
                    bot.send_video(user_id, message.video.file_id, caption=message.caption)
                    # Broadcast audio
                elif message.content_type == "audio":
                    bot.send_audio(user_id, message.audio.file_id, caption=message.caption)
                    # Broadcast documents
                elif message.content_type == "document":
                    bot.send_document(user_id, message.document.file_id, caption=message.caption)
                elif message.content_type == "sticker":
                    bot.send_sticker(user_id, message.sticker.file_id)
            except Exception as e:
                print(f"⭕️️Bu userga xabar jo'natilmadi. {user}: {e}")
            finally:
                broadcast_mode = False
        bot.send_message(message.chat.id, "Xabar yuborib tugallandi.")
    elif check_user_in_channel(message):
        try:
            file_kod = int(mmm)


            if file_kod <= anime_kod:
                bot.send_message(message.chat.id, "Searching....")
                file_n_i = get_file(file_kod)

                k = -1
                for f in file_n_i:
                    if f:
                        saved_file_id, file_name, file_type = f
                        k += 1
                        # Send file using its file_id

                        if file_type == 'photo':
                            bot.send_photo(message.chat.id, saved_file_id, caption= file_name)

                        elif file_type == 'video':
                            bot.send_video(message.chat.id, saved_file_id, caption= f"{k} - qism")

                        else:
                            bot.reply_to(message, "⭕️Unknown file type.")
                    else:
                        bot.reply_to(message, "⭕️File not found.")
            else:
                bot.send_message(message.chat.id, "🙁Bu kod bizning ro'yhatimizda topilmadi.")
        except ValueError:
            ani_res_list = get_ani_kod(mmm.lower())
            l  = ""
            keyboard_ani = InlineKeyboardMarkup()
            for x in ani_res_list:
                l += f"{x[0]}:  {x[1]}\n"
                but1 = InlineKeyboardButton(text= x[1] , url = f"https://t.me/insta_animelar_bot?start={x[0]}")
                keyboard_ani.add(but1)
            bot.send_message(message.chat.id, text = "Natijalar" , reply_markup= keyboard_ani)


        except Exception as e:
            bot.send_message(message.chat.id, f"💥Tizimda xatolik vujudga keldi. Iltimos keyinroq qayta uruning: {e}")
    else:
        send_welcome(message)


setup_block_user()
setup_database_followers()
setup_database_file()
setup_admin()
setup_database()
print("Your bot is running")
bot.infinity_polling()
