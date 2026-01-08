import pandas as pd

def pop(bot, message, way_to_db):
    text = message.text.replace(' ', '').replace('/pop', '')
    count = 1

    if text != '':
        if not text.isdigit():
            bot.send_message(message.chat.id, "После команды должно идти число")
            return
        else:
            count = int(text)


    df = pd.read_csv(way_to_db, encoding="utf-8-sig")

    df_slice = df[df['chat_id'] == message.chat.id] #cutting
    df_slice = df_slice.sort_values('rate', ascending=False) #sorting
    df_slice = df_slice[:count] #cutting
    words = list(df_slice['word'])

    if len(words) == 0:
        bot.send_message(message.chat.id, f'Список слов пуст')
        return

    df = df.drop(df[ (df['word'].isin(words)) & (df['chat_id']==message.chat.id) ].index)
    df.to_csv(way_to_db, index=False, encoding="utf-8-sig")

    from commands.wordix.send_long import send_long_message
    send_long_message(bot, message.chat.id, f'Были успешно удалены слова:\n {", ".join(words)}')