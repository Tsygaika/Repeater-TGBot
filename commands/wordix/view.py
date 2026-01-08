import pandas as pd

def view(bot, message, way_to_db):
    text = message.text.replace(' ', '').replace('/view', '')
    count = 10

    if text != '':
        if not text.isdigit():
            bot.send_message(message.chat.id, "После команды должно идти число")
            return
        else:
            count = int(text)


    df = pd.read_csv(way_to_db, encoding="utf-8-sig")

    df = df[df['chat_id'] == message.chat.id] #cutting
    df = df.sort_values('rate', ascending=False) #sorting
    df = df[:count] #cutting
    words, rates = list(df['word']), list(df['rate'])

    if len(words) == 0:
        bot.send_message(message.chat.id, f'Список слов пуст')
        return

    text = 'Результат запроса:\n'
    for i in range(len(df)):
        text += f'\n {words[i]} - {rates[i]}'

    from commands.wordix.send_long import send_long_message
    send_long_message(bot, message.chat.id, text + '\n\n')