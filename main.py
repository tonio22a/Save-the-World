import telebot
import random
from facttips import FACTS, TIPS
import threading
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)

subscribed_users = set()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "Добро пожаловать! Меня зовут Карл. Моя задача - заставить людей спасти мир от глобального потепления.\n\n"
        "<b>Используй команды:</b>\n"
        "/tips - получить случайный совет\n"
        "/facts - узнать интересный факт\n"
        "/subscribe - подписаться на ежедневную рассылку\n"
        "/unsubscribe - отписаться от рассылки\n"
        "/whatit - информация, что такое глобальное потепление\n"
        "/globalnews - новости про глобальное потепление\n"
        "/creators - канал создателей",
        parse_mode='HTML')

@bot.message_handler(commands=['tips'])
def send_tip(message):
    tips = random.sample(TIPS, 3)
    response = "<b>🌱 3 совета:</b>\n\n" + "\n\n".join(f"▪️ {tip}" for tip in tips)
    bot.reply_to(message, response, parse_mode='HTML')

@bot.message_handler(commands=['facts'])
def send_fact(message):
    facts = random.sample(FACTS, 3)
    response = "<b>🌍 3 факта:</b>\n\n" + "\n\n".join(f"▪️ {fact}" for fact in facts)
    bot.reply_to(message, response, parse_mode='HTML')

@bot.message_handler(commands=['subscribe'])
def subscribe_daily(message):
    user_id = message.chat.id
    if user_id not in subscribed_users:
        subscribed_users.add(user_id)
        bot.reply_to(message, "✅ Вы подписались на ежедневную рассылку! Рассылка происходит раз в 24 часа.")
    else:
        bot.reply_to(message, "❌ Вы уже подписаны на рассылку!")

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    user_id = message.chat.id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        bot.reply_to(message, "🔕 Вы отписались от рассылки.")
    else:
        bot.reply_to(message, "ℹ️ Вы не были подписаны на рассылку.")

@bot.message_handler(commands=["globalnews"])
def whatit(message):
    link = "https://ria.ru/keyword_globalnoe_poteplenie/"
    response = f"<a href='{link}'>Перейди по данной ссылке</a>, чтобы узнать новости о глобальном потеплении"
    bot.reply_to(message, response, parse_mode='HTML')


@bot.message_handler(commands=["whatit"])
def whatit(message):
    link = "https://telegra.ph/CHto-takoe-globalnoe-poteplenie-05-04"
    response = f"<a href='{link}'>Перейди по данной ссылке</a>, чтобы узнать о глобальном потеплении"
    bot.reply_to(message, response, parse_mode='HTML')

@bot.message_handler(commands=["creators"])
def whatit(message):
    link = "https://t.me/projectauoff"
    response = f"<a href='{link}'>Перейди по данной ссылке</a>, чтобы попасть в канал создателей"
    bot.reply_to(message, response, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "unsubscribe")
def handle_unsubscribe(call):
    user_id = call.message.chat.id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        bot.answer_callback_query(call.id, "Вы отписались от рассылки!")
    else:
        bot.answer_callback_query(call.id, "Вы не были подписаны!")

def daily_mailing():
    while True:
        try:
            now = time.localtime()
            if now.tm_hour == 9 and now.tm_min == 0:
                for user in subscribed_users.copy():
                    try:
                        facts = random.sample(FACTS, 3)
                        tips = random.sample(TIPS, 3)
                        
                        message = "<b>🌍 Ежедневная экоподборка</b>\n\n"
                        message += "<b>Топ-3 факта:</b>\n" + "\n".join(f"▪️ {f}" for f in facts)
                        message += "\n\n<b>🌱 Топ-3 советов:</b>\n" + "\n".join(f"▪️ {t}" for t in tips)
                        
                        bot.send_message(user, message, 
                                      parse_mode='HTML',)
                    except Exception as e:
                        print(f"Ошибка отправки для {user}: {e}")
                        subscribed_users.discard(user)
                
                time.sleep(60)
            else:
                time.sleep(30)
        except Exception as e:
            print(f"Ошибка в рассылке: {e}")

mailing_thread = threading.Thread(target=daily_mailing)
mailing_thread.daemon = True
mailing_thread.start()

print("Бот работает!")
bot.infinity_polling()
