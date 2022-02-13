import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рандомное число")
    item2 = types.KeyboardButton("Как дела?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, <b>{0.first_name}</b>!\nЯ - бот <b>{1.first_name}</b>. Помочь с созданием числа или поболтаем?".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def communication(message):
    if message.chat.type == 'private':
        if message.text == 'Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Как дела?':

            # inline keyboard
            markup = types.InlineKeyboardMarkup(row_width=3)
            item_1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item_2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            item_3 = types.InlineKeyboardButton("В целом норм", callback_data='neutral')


            markup.add(item_1, item_2, item_3)

            bot.send_message(message.chat.id, 'Все супер, как сам?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю, что ответить :(')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Ну классно же))')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает, Бро. Держись! Помни: даже если тебя съели, у тебя все равно есть 2 выхода :))')
            elif call.data == 'neutral':
                bot.send_message(call.message.chat.id, 'Это хорошо. Главное, чтобы проблем не было. А удача тебя ещё настигнет :)')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как дела?",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))

# RUN
bot.polling(none_stop=True)