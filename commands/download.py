import pandas as pd

def download(bot, message, way_to_data):
    df = pd.read_csv(way_to_data, converters={'front_word': str, 'back_word': str})
    df = df.loc[df['tg_id'] == message.chat.id]
    df = df.loc[df['created_flag'] == False]

    file_content = ''
    for _, row in df.iterrows():
        file_content = file_content + row['front_word'] + ' - ' + row['back_word'] + '\n'

    with open('user_words.txt', 'w') as new_file:  # сохраняем все в файл
        new_file.write(file_content)

    bot.send_document(message.chat.id, open(r'user_words.txt', 'rb'))