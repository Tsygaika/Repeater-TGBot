from telebot import TeleBot, types
from random import *
import config
import os

from background import keep_alive

import telebot

import openpyxl

bot = TeleBot('7422012459:AAF6gJu-dmyvVD_GNk9vLO-bNXuQm3p9Uo8')

################ КОМАНДЫ ################ КОМАНДЫ ################
@bot.message_handler(commands=["start"])
def start(message):    
    markup = types.InlineKeyboardMarkup(row_width = 1)
    btn1 = types.InlineKeyboardButton(text = 'Добавить карточки', callback_data = 'add_cards')
    markup.add(btn1)
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, добро пожаловать в бота!", reply_markup = markup)


@bot.message_handler(commands=["add"])  #добавить карточку
def add(message):
    from commands.add_cards import add_cards
    add_cards(bot, message)


@bot.message_handler(commands=["create"])   #создать список
def create(message):
    from commands.create_pack import create_pack
    create_pack(bot, message)


@bot.message_handler(commands=["watch"])    #посмотреть список карточек
def watch(message):
    from commands.watch import watch
    watch(bot, message)


@bot.message_handler(commands=["repeat"])   #повторить карточки
def repeat(message):
    from commands.repeat import repeat
    repeat(bot, message)


@bot.message_handler(commands=["delpair"])   #повторить карточки
def delpair(message):
    from commands.delete_pair import delete_pair
    delete_pair(bot, message)


@bot.message_handler(commands=["showdata"])   #повторить карточки
def showdata(message):
    from commands.showdata import showdata
    showdata(bot, message)


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Список команд\n\n /add - добавить карточки в колоду\n/create - создать колоду"
                                      "\n/watch - посмотреть колоду\n/repeat - повторить слова\n/delpair - удалить пару слов")


@bot.message_handler(commands=["version"])
def version(message):
    bot.send_message(message.chat.id, 'Версия бота: 07092024')

################ ОБРАБОТКА КНОПОК ################
@bot.callback_query_handler(func = lambda call:True)
def buttons(call):
    bot.answer_callback_query(call.id)  #убираем загрузку на кнопке

    if call.data == 'add_cards':
        from commands.add_cards import add_cards
        add_cards(bot, call.message)

    elif call.data == 'create_pack':
        from commands.create_pack import create_pack
        create_pack(bot, call.message)

    elif call.data.startswith('add_word_to:'):  #если строка начинается с 'add_word', то нужно добавить слово в колоду
        from commands.add_word import add_word
        add_word(bot, call.message, call.data)

    #начало гайда в quizlet
    elif call.data.startswith('add_quizlet_to:'):
        from commands.quizlet_guide import quizlet_guide
        quizlet_guide(bot, call.message, call.data)

    elif call.data.startswith('prev_1:'):
        from commands.quizlet_guide import prev_1
        prev_1(bot, call.message, call.data)

    elif call.data.startswith('next_1:'):
        from commands.quizlet_guide import next_1
        next_1(bot, call.message, call.data)

    elif call.data.startswith('next_2:'):
        from commands.quizlet_guide import next_2
        next_2(bot, call.message, call.data)

    elif call.data.startswith('prev_2:'):
        from commands.quizlet_guide import prev_2
        prev_2(bot, call.message, call.data)

    elif call.data.startswith('next_2_3:'):
        from commands.quizlet_guide import next_2_3
        next_2_3(bot, call.message, call.data)

    elif call.data.startswith('prev_3:'):
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id) #из-за того, что мы ждали сообщение от
                                    #пользователя, но он вернулся, нам нужно перестать ждать от него сообщение
        from commands.quizlet_guide import next_1   #назад с 3 шага то же самое, что вперед с 1 шага
        next_1(bot, call.message, call.data)

    elif call.data.startswith('packname:'):
        markup = types.InlineKeyboardMarkup(row_width=1)
        call_data = call.data.replace('packname:', '') #убираем 'packname:' и сохраняем текст в call.data
        btn1 = types.InlineKeyboardButton(text='Слово', callback_data= 'add_word_to:' + call_data)  # сохраним также
        btn2 = types.InlineKeyboardButton(text='Карточки из Quizlet', callback_data='add_quizlet_to:' + call_data)  # название колоды
        markup.add(btn1, btn2)
        bot.edit_message_text('Что нужно добавить?', call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)

    elif call.data.startswith('watch:'):
        from commands.watch import open_pack
        open_pack(bot, call)

    elif call.data.startswith('showdata:'):
        from commands.showdata import open_pack
        open_pack(bot, call)

    elif call.data.startswith('repeat:'):
        from commands.repeat import repeat_2
        repeat_2(bot, call)

    elif call.data.startswith('check:'):
        from commands.repeat import repeat_3
        repeat_3(bot, call)

    elif call.data.startswith('delete:'):
        from commands.delete_pair import delete_pair_2
        delete_pair_2(bot, call)

    elif call.data.startswith(('easy:', 'medium:', 'hard:', 'again:')):
        from commands.repeat import edit
        edit(bot, call)

    else:   #иначе это названия его колод
        bot.send_message(call.message.chat.id, "произошло исключение")
        print('ИСКЛЮЧЕНИЕ')


#webhook####################### НЕ ТРОГАТЬ!!!###################
keep_alive()  #запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.infinity_polling(none_stop=True)
#запуск бота