import pandas as pd
from telebot import types
#это можно объединить с showdata через использование флага
def watch(bot, message, way_to_data):
    from commands.get_packs_list import get_packs_list
    pack_list = get_packs_list(message, way_to_data)

    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(pack_list)):
        btn = types.InlineKeyboardButton(text=pack_list[i], callback_data='watch:' + str(pack_list[i]))
        markup.add(btn)

    if len(pack_list) == 0:  # если нет колод
        btn = types.InlineKeyboardButton(text='+ создать колоду', callback_data='create_pack')
        markup.add(btn)
        bot.send_message(message.chat.id, 'У вас нет колод', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Ваши колоды', reply_markup=markup)


def open_pack(bot, call, way_to_data):
    call_data = call.data.replace('watch:', '')  # убираем префикс
    message = call.message

    df = pd.read_csv(way_to_data, converters={'pack_name': str, 'front_word': str, 'back_word': str})
    df = df.loc[df['tg_id'] == message.chat.id]  # обрезаем по id
    df = df.loc[df['pack_name'] == call_data]
    df = df.loc[df['created_flag'] == False]

    if df.empty:  # если колода пустая
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton(text='+ добавить слова', callback_data='packname:' + call_data)
        markup.add(btn)

        bot.edit_message_text(f'Колода {call_data} пуста', message.chat.id, message_id=message.message_id,
                              reply_markup=markup)
    else:
        words_list = ''  # список пар слов
        for _, row in df.iterrows():
            words_list = words_list + '\n' + row['front_word'] + ' - ' + row['back_word'] # добавляем оба слова

        bot.edit_message_text(f'Колода {call_data}: ' + words_list[:4000], message.chat.id,
                              message_id=message.message_id)
        words_list = words_list[4000:]
        while len(words_list) >= 4000:
            bot.send_message(message.chat.id, words_list[:4000])
            words_list = words_list[4000:]