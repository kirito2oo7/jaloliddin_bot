from telebot import types
import sqlite3
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot

API_key = "7875456211:AAG60eGvXGcnTHobLahwPxKVCBVIcr2Zx4Y"



bot = telebot.TeleBot(API_key)
bmd = "CAACAgIAAxkBAAIBlmdxZi6sK42VCA3-ogaIn30MXGrmAAJnIAACKVtpSNxijIXcPOrMNgQ"

def is_admin(user_id):
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins")
    ids_of_admin = cursor.fetchall()
    for x in ids_of_admin:
        if user_id == x[1]:
            return True
    return False


def main_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin(message.chat.id):
        item_bh = types.KeyboardButton(text="🛂Boshqaruv")
        markup.row(item_bh)
    return markup

def get_file(file_kod):
    conn = sqlite3.connect("bot_file.db")
    cursor = conn.cursor()
    cursor.execute('SELECT  file_id, file_name, file_type FROM files WHERE file_kod = ?', (file_kod,))
    file = cursor.fetchall()
    conn.close()
    return file

def check_user_in_channel(message):
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


def log_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect("bot_file.db", check_same_thread=False)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        """, (user_id, username, first_name, last_name))
        conn.commit()

    except sqlite3.Error as e:
        print("Error logging user:", e)
    finally:
        conn.close()



def handle_start_button(call):
    bot.answer_callback_query(call.id, "Sending /start command...")
    print(check_user_in_channel(call.message))
    if check_user_in_channel(call.message):
        conn = sqlite3.connect("bot_file.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM followers")
        ll = cursor.fetchall()
        for chan in ll:
            s:str = chan[2]
            n: int = chan[4]
            print(s,n)
            cursor.execute("UPDATE followers SET now_follower = ? WHERE channel_url = ?", (n + 1, s))
            conn.commit()
            m:int = chan[3]
            if n >= m:
                cursor.execute("DELETE FROM followers WHERE channel_url = ?", (s,))
                conn.commit()

                bot.send_message(call.message.chat.id, f"✅ {chan[1]} kanal {n} ta obunachi qo'shilgani uchun o'chirildi")





def send_welcome(message: types.Message):
    args = message.text.split()

    user = message.from_user

    log_user(user.id, user.username, user.first_name, user.last_name)
    file_kod = None


    if check_user_in_channel(message):

        bot.send_message(message.chat.id,"Assalomu alaykum, bu Isnta animelar  boti.Kerakli anime kodi yuboring...", reply_markup=main_keyboard(message))
        try:
            if len(args) > 1 and int(args[1]) < 1e8:
                file_kod = int(args[1])
                bot.send_message(message.chat.id, "Searching....")
                file_n_i = get_file(file_kod)

                k = -1
                for f in file_n_i:
                    if f:
                        saved_file_id, file_name, file_type = f
                        k += 1
                        # Send file using its file_id

                        if file_type == 'photo':
                            bot.send_photo(message.chat.id, saved_file_id, caption=file_name)

                        elif file_type == 'video':
                            bot.send_video(message.chat.id, saved_file_id, caption=f"{k} - qism")

                        else:
                            bot.reply_to(message, "⭕️Unknown file type.")
                    else:
                        bot.reply_to(message, "⭕️File not found.")

        except Exception as e:
            print(e)
        finally:
            print("----")

    else:
        try:
            if len(args) > 1 and int(args[1]) < 1e8:
                file_kod = f"\n📌Po'stadgi animeni ko'rish uchun {int(args[1])} kodini yozing."
            else:
                file_kod = ""
        except:
            file_kod = ""
        conn = sqlite3.connect("bot_file.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM followers")
        l = cursor.fetchall()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("📱 Instagram", url="https://instagram.com/anipower_uz/"))
        for c in l:
            print("c =", c[1], c[2])
            keyboard.add(InlineKeyboardButton(text= c[1], url= c[2]))

        start_button = InlineKeyboardButton("✅Tekshirish", callback_data="send_start")
        keyboard.add(start_button)

        bot.send_message(message.chat.id, f"Assalomu alaykum \nAgar bizning xizmatlarimizdan foydalanmoqchi bo'lsangiz, Iltimos pastdagi kanallarga obuna bo'ling!{file_kod}",reply_markup=keyboard)
        bot.send_sticker(message.chat.id, sticker = bmd)






