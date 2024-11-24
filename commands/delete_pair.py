import pandas as pd
from telebot import types

def delete_pair(bot, message, way_to_data):
    df = pd.read_csv(way_to_data, converters={'pack_name': str, 'front_word': str, 'back_word': str})

    from commands.get_packs_list import get_packs_list
    packs_list = get_packs_list(message, way_to_data)

    if len(packs_list) == 0:    #если нет колод
        bot.send_message(message.chat.id, 'Вы не можете удалить пару слов, так как у вас не колод')
        return


    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in range(0, len(packs_list)):
        btn = types.InlineKeyboardButton(text=packs_list[i], callback_data='delete:' + str(packs_list[i]))
        markup.add(btn)

    bot.send_message(message.chat.id, 'Ваши колоды', reply_markup=markup)


def delete_pair_2(bot, call, way_to_data):
    bot_message = bot.edit_message_text('Отправьте первое слово в паре, которую нужно удалить',
                                        call.message.chat.id, message_id=call.message.message_id)

    bot.register_next_step_handler(call.message, delete_pair_3, bot, call, way_to_data)

def delete_pair_3(message, bot, call, way_to_data):
    first_word = message.text   #получаем первое слово из пары, которую нужно удалить
    call_data = call.data.replace('delete:', '')  # убираем префикс
    message = call.message

    df = pd.read_csv(way_to_data, converters={'pack_name': str, 'front_word': str, 'back_word': str})
    copy_df = df
    df = df.loc[df['tg_id'] == message.chat.id]  # оставляем колоды только этого пользователя
    df = df.loc[df['pack_name'] == call_data]  # оставляем только слова из одной колоды

    ind = df[df['front_word'] == first_word].index.tolist()
    if len(ind) == 0:
        bot.edit_message_text('Такой пары в колоде нет', message.chat.id, message_id=message.message_id)

    else:
        second_word = copy_df.loc[ind[0], 'back_word']

        copy_df.drop(ind[0], inplace=True)
        copy_df.to_csv(way_to_data, index=False, encoding="utf-8-sig")  # сохраняем df
        bot.edit_message_text(f'Пара {first_word} - {second_word} удалена', message.chat.id, message_id=message.message_id)