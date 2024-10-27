from telebot import TeleBot, types

def add_cards(bot, message, way_to_data):
    from commands.get_packs_list import get_packs_list
    packs_list = get_packs_list(message, way_to_data)

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup = types.InlineKeyboardMarkup(row_width=1)

    for i in range(0, len(packs_list)):
        btn = types.InlineKeyboardButton(text=packs_list[i], callback_data='packname:' + str(packs_list[i]) )
        markup.add(btn)

    btn = types.InlineKeyboardButton(text='+ создать колоду', callback_data='create_pack')
    markup.add(btn)

    try:    #в main эта функция используется дважды по-разному
        bot.edit_message_text('Ваши колоды', message.chat.id, message_id=message.message_id, reply_markup=markup)

    except Exception:
        bot.send_message(message.chat.id, 'Ваши колоды', reply_markup=markup)