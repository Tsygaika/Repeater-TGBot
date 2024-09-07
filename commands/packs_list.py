from telebot import TeleBot, types

def packs_list(bot, message, sheet):
    
    markup = types.InlineKeyboardMarkup(row_width = 1)

    if sheet[0 + 1][0 + 0].value != None: #если есть хоть одна колода
        i = 0
        
        while i < sheet.max_column + 1:
            btn = types.InlineKeyboardButton(text = sheet[0 + 1][i + 0].value, callback_data = 'packname:' + sheet[0 + 1][i + 0].value)
            markup.add(btn)
            i += 10

    btn = types.InlineKeyboardButton(text = '+ создать колоду', callback_data = 'create_pack')
    markup.add(btn)

    try:
        bot.edit_message_text('Ваши колоды', message.chat.id, message_id = message.message_id, reply_markup = markup)

    except Exception:
        bot.send_message(message.chat.id, 'Ваши колоды', reply_markup=markup)