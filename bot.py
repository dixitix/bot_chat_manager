import telebot
from telebot import types

bot = telebot.TeleBot("5535467636:AAFZ84W5iWEx1__TzvvBVjmdEtX5MvdN1O8")


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}! Я бот, который поможет вам организовать чат :)'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(content_type='new_chat_members')
def welcome(message):
    mess = f'Привет, {message.from_user.first_name}! Добро пожаловать в чат!'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['help'])
def help_(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    promote_button = types.InlineKeyboardButton(text="Сделать пользователя админом", callback_data='promote')
    ban_button = types.InlineKeyboardButton(text="Забанить пользователя", callback_data='ban')
    unban_button = types.InlineKeyboardButton(text="Разбанить пользователя", callback_data='unban')
    get_statistics_button = types.InlineKeyboardButton(text="Вывести статистику по админам",
                                                       callback_data='get_statistics')
    kick_the_bot_button = types.InlineKeyboardButton(text="Удалиться из чата", callback_data='kick_the_bot')
    keyboard.add(promote_button, ban_button, unban_button, get_statistics_button, kick_the_bot_button)
    bot.send_message(message.chat.id, "Я умею делать вот такие команды:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "promote":
        bot.send_message(call.message.chat.id,
                         f'Ответьте на сообщение пользователя, которого нужно повысить, кодовым словом "повысить"')
    elif call.data == "ban":
        bot.send_message(call.message.chat.id,
                         f'Ответьте на сообщение пользователя, которого нужно забанить, кодовым словом "забанить"')
    elif call.data == "unban":
        bot.send_message(call.message.chat.id,
                         f'Ответьте на сообщение пользователя, которого нужно разбанить, кодовым словом "разбанить"')
    elif call.data == "get_statistics":
        count_administrators = 0
        for member in bot.get_chat_administrators(call.message.chat.id):
            count_administrators += 1
        bot.send_message(call.message.chat.id,
                         f"Количество администраторов: {count_administrators} \n"
                         f"Количество обычных пользователей: {bot.get_chat_members_count(call.message.chat.id) - count_administrators}")
    elif call.data == "kick_the_bot":
        bot.leave_chat(call.message.chat.id)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "повысить":
        bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.send_message(message.chat.id, f"Этот пользователь теперь админ")

    if message.text == "забанить":
        bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.send_message(message.chat.id, f"Этот пользователь теперь забанен")

    if message.text == "разбанить":
        bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.send_message(message.chat.id,
                         f"Этот пользователь разбанен. Он может снова вступить в чат")


bot.polling(none_stop=True)
