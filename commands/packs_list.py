from telebot import TeleBot, types

def packs_list(bot, message, sheet):
    #pack_list = []  #список с названиями всех колод
    
    markup = types.InlineKeyboardMarkup(row_width = 1)
    
    if sheet[0 + 1][0 + 0].value != None: #если есть хоть одна колода
        i = 0
        
        while i < sheet.max_column + 1:
            btn = types.InlineKeyboardButton(text = sheet[0 + 1][i + 0].value, callback_data = sheet[0 + 1][i + 0].value)
            markup.add(btn)
            #pack_list.append(sheet[0 + 1][i + 0].value)
            i += 10

    btn = types.InlineKeyboardButton(text = '+ создать колоду', callback_data = 'create_pack')
    markup.add(btn)
    #bot.send_message(message.chat.id, f"Текущие колоды", reply_markup=markup)
    bot.edit_message_text('Текущие колоды', message.chat.id, message_id = message.message_id, reply_markup = markup)
    
