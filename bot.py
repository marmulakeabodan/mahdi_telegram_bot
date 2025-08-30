import telebot

# توکن تستی شما (برای ربات اصلی حتماً توکن جدید بگیر از BotFather)
TOKEN = "8233889241:AAG12Wt7vHeCEsZvMloYoEbsj7X9iSHErd8"

bot = telebot.TeleBot(TOKEN)

# وضعیت کاربران (برای نگهداری موقت اسم/فامیل)
user_state = {}

# شروع ربات
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_state[chat_id] = {'step': 'first'}
    bot.send_message(chat_id, "سلام 👋\nلطفاً اسم خودت رو بنویس:")

# گرفتن پیام‌ها
@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_state:
        bot.send_message(chat_id, "برای شروع لطفاً دستور /start رو بزن.")
        return

    step = user_state[chat_id]['step']

    if step == 'first':
        # ذخیره نام
        user_state[chat_id]['first_name'] = text
        user_state[chat_id]['step'] = 'last'
        bot.send_message(chat_id, "خیلی خوب ✅ حالا فامیلی‌ات رو بنویس:")

    elif step == 'last':
        # ذخیره فامیل
        user_state[chat_id]['last_name'] = text
        first = user_state[chat_id]['first_name']
        last = user_state[chat_id]['last_name']

        # ذخیره در فایل متنی
        with open("users.txt", "a", encoding="utf-8") as f:
            f.write(f"{first} {last}\n")

        # نمایش نتیجه به کاربر
        bot.send_message(chat_id, f"اطلاعات شما ثبت شد 📋:\n\nنام: {first}\nفامیل: {last}\n\n✅ در فایل users.txt ذخیره شد.")

        # پاک کردن وضعیت
        del user_state[chat_id]

# اجرای ربات
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.infinity_polling()