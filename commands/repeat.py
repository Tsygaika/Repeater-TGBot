from datetime import datetime, timedelta
from telebot import types
from math import floor
import pandas as pd
from random import randint

def repeat(bot, message, way_to_data):
    from commands.get_packs_list import get_packs_list
    pack_list = get_packs_list(message, way_to_data)

    df = pd.read_csv(way_to_data, parse_dates=['date_of_repeat'],
                     converters={'pack_name': str, 'front_word': str, 'back_word': str})
    df = df.loc[df['tg_id'] == message.chat.id]  # оставляем колоды только этого пользователя
    df = df.loc[df['created_flag'] == False]    #убираем тех.инфу
    df = df[pd.to_datetime(df['date_of_repeat']) <= datetime.now()]  # отсеиваем по времени

    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(pack_list)):
        copy_df = df
        copy_df = df.loc[df['pack_name'] == pack_list[i]]   #считаем количество слов для каждой колоды

        btn = types.InlineKeyboardButton(text=f"{pack_list[i]} [{copy_df.shape[0]}]", callback_data='repeat:' + str(pack_list[i]))
        markup.add(btn)

    if len(pack_list) == 0:  # если нет колод
        btn = types.InlineKeyboardButton(text='+ создать колоду', callback_data='create_pack')
        markup.add(btn)
        bot.send_message(message.chat.id, 'У вас нет колод', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Ваши колоды', reply_markup=markup)


def repeat_2(bot, message, pack_name, way_to_data):
    df = pd.read_csv(way_to_data, parse_dates=['date_of_repeat'],date_format='%Y-%m-%d',converters={'pack_name': str, 'front_word': str, 'back_word': str})
    df = df.loc[df['tg_id'] == message.chat.id]  # оставляем колоды только этого пользователя
    df = df.loc[df['pack_name'] == pack_name]
    df = df.loc[df['created_flag'] == False]
    df = df[pd.to_datetime(df['date_of_repeat']) <= datetime.now()] #отсеиваем по времени

    if  df.empty:
        bot.edit_message_text(f'В колоде {pack_name} нечего повторять', message.chat.id, message_id=message.message_id)
        return
    else:
        rand = randint(0, df.shape[0] - 1)
        row = df.iloc[rand]

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton(text='Проверить', callback_data=f"check:{row['pack_name']}:{row['front_word']}")
        markup.add(btn)
        bot.edit_message_text(f"[{df.shape[0]}] Вспомните пару к слову\n\n<b>{row['front_word']}\n \nㅤ</b>", message.chat.id,
                              message_id=message.message_id, parse_mode='HTML', reply_markup=markup)


def repeat_3(bot, call, way_to_data):
    message = call.message

    df = pd.read_csv(way_to_data, date_format='%Y-%m-%d', parse_dates=['date_of_repeat'],converters={'pack_name': str, 'front_word': str, 'back_word': str})

    df['date_of_repeat'] = pd.to_datetime(df['date_of_repeat'], format='%Y-%m-%d', errors='coerce')
    df = df.loc[df['tg_id'] == call.message.chat.id]  # оставляем колоды только этого пользователя
    name, front_word = call.data.replace('check:', '').split(':')
    df = df.loc[df['pack_name'] == name]
    df = df.loc[df['created_flag'] == False]    #эта строка и ниже чисто, чтобы получить правильное количество строк
    df = df[pd.to_datetime(df['date_of_repeat']) <= datetime.now()]  # отсеиваем по времени
    rows = df.shape[0]
    df = df.loc[df['front_word'] == front_word]

    row = df.iloc[0]
    back_word = row['back_word']

    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton(text='Легко', callback_data=f'easy:{name}:{front_word}')
    btn2 = types.InlineKeyboardButton(text='Средне', callback_data=f'medium:{name}:{front_word}')
    btn3 = types.InlineKeyboardButton(text='Сложно', callback_data=f'hard:{name}:{front_word}')
    btn4 = types.InlineKeyboardButton(text='Повторить еще раз', callback_data=f'again:{name}:{front_word}')
    markup.add(btn1, btn2, btn3, btn4)

    bot.edit_message_text(f'[{rows}] Проверка\n<b>{front_word}</b> - <b>{back_word}</b>\n'
                          f'Насколько легко было вспомнить?', message.chat.id, message_id=message.message_id, parse_mode='HTML',
                          reply_markup=markup)


def edit(bot, call, way_to_data):
    message = call.message

    df = pd.read_csv(way_to_data, parse_dates=['date_of_repeat'], date_format='%Y-%m-%d',converters={'pack_name': str, 'front_word': str, 'back_word': str})
    copy_df = df
    df = df.loc[df['tg_id'] == call.message.chat.id]  # оставляем колоды только этого пользователя
    react, name, front_word = call.data.split(':')
    df = df.loc[df['pack_name'] == name]
    df = df.loc[df['front_word'] == front_word]

    row = df.iloc[0]
    repeat_length = row['repeat_length']    #получаем предыдущий промежуток

    #в первые 3 этапа повторения кнопки(кроме again) не имеют значения
    if react == 'easy' or (repeat_length < 5 and (react == 'medium' or react == 'hard')):
        new_gap = 1.5 * repeat_length + 1 #считаем по формуле y=2.5x+1, но в этой формуле отсчет от начала, а у меня
                                      #относительный, поэтому я вычитаю prev_gap

    elif react == 'medium' and repeat_length > 5:
        new_gap = (repeat_length - 1) / 1.5  #получаем предыдущее значение промежутка

    elif react == 'hard' and repeat_length > 5:
        new_gap = ((repeat_length - 1) / 1.5 - 1) / 1.5  #откатываем промежуток на два значения назад

    elif react == 'again': #в зависимости от того, какую оценку получило слово, будем менять интервал
        new_gap = 0 #сбрасываем промежуток
    else:
        bot.send_message(message.chat.id, "<code>Ошибка №8 в файле repeat</code>\nСообщить об ошибке @Tsygaika",
                         parse_mode='HTML')
        return

    try:
        ind = df[df['front_word'] == front_word].index.tolist()[0]
        copy_df.loc[ind, 'date_of_repeat'] = datetime.now().date() + timedelta(days=floor(new_gap))
        copy_df.loc[ind, 'repeat_length'] = new_gap
        copy_df.to_csv(way_to_data, index=False)  # сохраняем df

        repeat_2(bot, message, name, way_to_data)

    except Exception as e:
        bot.send_message(message.chat.id, f"<code>Ошибка №9 в файле repeat</code>\nСообщить об ошибке @Tsygaika\n\n Код ошибки{e}",
                         parse_mode='HTML')


# def check_for_todays_date(sheet, i): #проверяем нет ли в колоде еще сегодняшней даты(может быть, если нажать again)
#     j = 2
#     while sheet[j + 1][i + 0].value != None:  # идем по списку пока не будет первая пустая строка
#         if (sheet[j + 1][i + 2 + 0].value - datetime.datetime.now()).days < 0:
#             return j - 1 #так как next_word начинает искать слова со след., то, чтобы найти данное слово, нужно указать на пред.
#
#         j+=1
#
#     return -1
#
#
# def next_word(bot, message, i ,j, way_to_data):
#
#     # по стандарту ищем лист с id человека
#     book = openpyxl.open(way_to_data)
#     sheets_list = book.sheetnames
#
#     for _ in sheets_list:
#         if _ == str(message.chat.id):
#             sheet = book[_]
#             book.active = book[_]  # задаем новую активную страницу
#             break
#
#
#     j+=1    #начинаем сразу со следующего слова
#     repeat_flag = 1
#     while sheet[j + 1][i + 0].value != None:  # идем по списку пока не будет первая пустая строка
#
#         if (sheet[j + 1][i + 2 + 0].value - datetime.datetime.now()).days < 0:
#             repeat_flag = 0  # если хоть одно слово было выведено, то меняем флаг
#
#             markup = types.InlineKeyboardMarkup(row_width=1)
#             btn = types.InlineKeyboardButton(text='Проверить', callback_data=f'check:{i}:{j}')
#             markup.add(btn)
#
#             bot.edit_message_text(f'Вспомните пару к слову\n\n<b>{sheet[j + 1][i + 0].value}</b>', message.chat.id,
#                                   message_id=message.message_id, parse_mode='HTML', reply_markup=markup)
#             book.close()
#             return
#
#         j += 1
#
#     if repeat_flag:
#         j = check_for_todays_date(sheet, i)     #если есть еще слово с сегодняшней датой
#         if j != -1:
#             next_word(bot, message, i, j, way_to_data)
#         else:
#             bot.edit_message_text('Больше карточек на сегодня нет', message.chat.id, message_id=message.message_id)
#
#     book.close()