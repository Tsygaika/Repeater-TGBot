from telebot import TeleBot, types
from random import *
import config
import os

from background import keep_alive

import telebot

import openpyxl

bot = TeleBot('7422012459:AAF6gJu-dmyvVD_GNk9vLO-bNXuQm3p9Uo8')

###########################################
@bot.message_handler(commands=["start"])
def start(message):    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text = 'Добавить карточки', callback_data = 'add_cards')
    markup.add(btn1)
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, добро пожаловать в бота!", reply_markup = markup)
    


@bot.callback_query_handler(func = lambda call:True)
def buttons(call):      #ОБРАБОТКА КНОПОК
    if call.data == 'add_cards':
        bot.answer_callback_query(call.id)

        book = openpyxl.open("data.xlsx")
        sheets_list = book.sheetnames #получаем список листов
        
        for i in sheets_list:#ищем лист беседы
            if i == str(call.message.chat.id):
                sheet = book[i]
                book.active = book[i]#задаем новую активную страницу
                break
            
        else:           #если листа для такой беседы нет, то создаем
            book.create_sheet(str(call.message.chat.id))
            book.active = book[str(call.message.chat.id)]
            sheet = book.active

            '''link = sheet.cell(row = 1 + 1, column = 0 + 1)#saving based info to file
            link.value = 'front'
            link = sheet.cell(row = 1 + 1, column = 1 + 1)
            link.value = 'back'
            link = sheet.cell(row = 1 + 1, column = 2 + 1)
            link.value = 'description'
            link = sheet.cell(row = 0 + 1, column = 1 + 1)
            link.value = "<-pack's name"'''

        book.save('data.xlsx')#сохраняем

        from commands.packs_list import packs_list
        packs_list(bot, call.message, sheet)
        #bot.edit_message_text('Кнопка обработана', call.message.chat.id, message_id = call.message.message_id)

    #else:
        
###группа##################################
'''@bot.message_handler(commands=["join"])
def comm1(message):
  if len(message.text) == 5:
    spis.append(str(message.from_user.first_name))
  else:
    spis.append(str(message.text.replace("/join", "")))
  bot.reply_to(message, "Добавил!")

@bot.message_handler(commands=["list", "spis"])
def comm2(message):
  if len(spis) <= 0:
    bot.reply_to(message, "Список пуст!")
  else:
    spisstr = ''
    for i in range(0, len(spis)):
      spisstr = spisstr + f"<b>{i+1}.</b> " + spis[i] + "\n"
      bot.reply_to(message, spisstr, parse_mode='HTML')

@bot.message_handler(commands=["leave"])
def comm3(message):
  if len(message.text) == 6 and any(
      str(message.from_user.first_name) in i for i in spis):
    for i in range(0, len(spis)):
      if str(message.from_user.first_name) in spis[i]:
        spis.pop(i)
        bot.reply_to(message, "Удалил!")
        break
  elif str(message.text).replace("/leave ", "").isdigit() == True:
    if 0 < int(message.text.replace("/leave ", "")) <= len(spis):
      spis.pop(int(message.text.replace("/leave ", "")) - 1)
      bot.reply_to(message, "Удалил!")
    else:
      bot.reply_to(message, "Такого номера нет в списке")
  else:
    bot.reply_to(message, "Что-то ты написал не так")

@bot.message_handler(commands=["listwi", "spiswi"])
def comm4(message):
  if len(spis) <= 0:
    bot.reply_to(message, "Список пуст!")
  else:
    a8 = randint(0, len(spis) - 1)
    bot.reply_to(message,f"<b>{spis[a8] }</b> " + message.text.replace("/listwi", "").replace("/spiswi", ""),parse_mode='HTML')

@bot.message_handler(commands=["clear"])
def comm5(message):
  spis.clear()
  bot.reply_to(message, "Список очищен!")

###распознавание текст. сообщ.#############
@bot.message_handler(content_types=["text"])
def mess(message):
    saved_text = message.text
    message.text = message.text.lower()
    
    #добавление shortcut
    if message.text.startswith(("/addshortcut", "/addsc")):
        from commands.addshortcut import add_short_cut
        add_short_cut(bot, message, message.text)

    #удаление shortcut
    elif message.text.startswith(("/deletesc", "/dltsc")):
        from commands.delete_sc import delete_sc_func
        delete_sc_func(bot, message, message.text)

    #лист shortcut
    elif message.text.startswith(("/listsc", "/sclist")):
        from commands.shortcutslist import shortcuts_list
        shortcuts_list(bot, message)

    #перевод текста
    elif message.text.startswith(("@jerrix2bot t", "/t", "/trans", "/translate")):
        from commands.translate import translate_func
        translate_func(bot, message)
  
    #монетка
    elif message.text.startswith(("/c", "/coin")):
        from commands.coin import coin_func
        bot.reply_to(message, coin_func(), parse_mode='HTML')
  
    #кто тут...
    elif message.text.startswith(("/whois", "/wi", "@jerrix2bot кто")):
        from commands.whois import whois_func
        name, text = whois_func(message)
        bot.reply_to(message,"<b>{}</b>{}".format(name, text),parse_mode='HTML')

    #число от до
    elif message.text.startswith(("@jerrix2bot число", "@jerrix2bot n", "@jerrix2bot num","@jerrix2bot number", "/n ", "/num", "/number")):
        from commands.number import number_func
        number_func(bot, message)
    
    #инфо о сообщении
    elif message.text.startswith(("/data")):
        from commands.data import data_func
        data_func(bot, message)
  
    #бросание кубика
    elif message.text.startswith(("бросить кубик", "подбросить кубик", "/cube", "/cu")):
        bot.send_dice(message.chat.id, "🎲")
    
    #..ли..
    elif ("ли" in message.text) and ("или" not in message.text) and ("@jerrix2bot" in message.text) and ("@jerrix2botли" not in message.text.replace(" ", "")):
        from commands.li import li_func
        li_func(bot, message)
      
    #/bb пока
    elif message.text.startswith(("/bb")):
        from commands.bb import bb_func
        bb_func(bot, message)
      
    #да-нет
    elif message.text.startswith(("/dn", "/danet")):
        from commands.danet import danet_func
        danet_func(bot, message)
    
    #или
    elif (message.text.startswith("/ili") and ("," in message.text)) or (message.text.startswith(("@jerrix2bot")) and ("или" in message.text)):
        from commands.ili import ili_func
        ili_func(bot, message)
    
    #@all
    elif ("@all" in message.text):
        from commands.all import all_func 
        all_func(bot, message)

    #ауф
    elif (message.text.startswith(("/auf"))):
        from commands.auf import auf_func 
        auf_func(bot, message)
    
    #жак фреско и другие картинки
    elif (message.text.startswith(("/stethem","/stet","/fresko"))) or (message.chat.id == -1001868800871 and (message.text.startswith(("/sasha","/maga","/sult","/alex")))):
        from commands.fresko import fresko_func
        fresko_func(bot, message)

    elif (message.text.startswith(("/version"))):
        bot.reply_to(message,'1.0.0')
        
    #голос в текст
    elif (message.text.startswith(("/v", "/voice"))) or (((message.text[0] == 'v') or(message.text[0] == 'в'))and len(message.text) == 1):
        from commands.voice import voice_func
        voice_func(bot, message)

    #команда остановки
    elif (message.text.startswith(("/stop"))):
        from commands.stop import stop_func 
        stop_func(bot, message)

    #обработка всех shortcuts
    else:
        from commands.shortcuts import shortcuts_func
        shortcuts_func(bot, message)

from commands.parser import parser_func
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(parser_func, 'interval', seconds = 10, args = [bot])'''
        
###ответ на стикеры#############
'''@bot.message_handler(content_types=["sticker"])
def text(message):
    probability = randint(1,10)
    if probability == 1:
      var = randint(1,3)
      if var == 1:
          bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEaSdmCaIAAUWhiBfLkRnXOPaYc8LX6-8AAvoYAAJQselJ9IYFSIVBjlY0BA')
      elif var == 2:
          bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEaSNmCaGA_vSyxfRwy3NgpKUGcJ6cpQAClhEAAv5tgEmdX9KNHziRpTQE')
      elif var == 3:
          bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEaSRmCaGAxaRyUeXsONF3mokBp_9mugAC4yYAAqS7uUt-72DEdMZK8zQE')'''

#bot.forward_message(-1001933961555, message.chat.id, message.reply_to_message.id)
#webhook####################### НЕ ТРОГАТЬ!!!###################
keep_alive()  #запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.infinity_polling(none_stop=True)
#запуск бота
