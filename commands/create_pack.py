from telebot import types
import pandas as pd

def create_pack(bot, message, way_to_data):
    try:
        bot_message = bot.edit_message_text('Отправьте название колоды', message.chat.id, message_id = message.message_id)
    except Exception:
        bot_message = bot.send_message(message.chat.id, 'Отправьте название колоды')

    bot.register_next_step_handler(message, create_pack_2, bot, bot_message, way_to_data)

def create_pack_2(message, bot, bot_message, way_to_data):
    from commands.get_packs_list import get_packs_list     #получаем список уже имеющихся колод
    packs_list = get_packs_list(message, way_to_data)

    print(message.text, packs_list)
    if message.text in packs_list:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton(text='Изменить название', callback_data='create_pack')
        markup.add(btn)

        bot.edit_message_text('Колода с таким названием уже есть', message.chat.id, message_id=bot_message.message_id, reply_markup = markup)
        bot.delete_message(message.chat.id, message.message_id)
        return

    df = pd.read_csv(way_to_data, converters={'pack_name' : str,'front_word' : str,'back_word' : str})
    df.loc[len(df)] = [message.chat.id, message.text,True,'','',0,0]    #добавили техническую строку
    df.to_csv(way_to_data, index=False) #сохраняем df


    markup = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton(text='Добавить карточки', callback_data='packname:' + message.text)
    markup.add(btn)

    bot.edit_message_text(f'Колода «{message.text}» создана', bot_message.chat.id, message_id = bot_message.message_id, reply_markup = markup)