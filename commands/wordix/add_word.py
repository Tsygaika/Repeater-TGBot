import pandas as pd
from telebot.types import ReactionTypeEmoji

def add_word(bot, message, way_to_db):
    chat_id, word = message.chat.id, message.text
    df = pd.read_csv(way_to_db, encoding="utf-8-sig") # , converters={'rate' : int}


    slice = df[(df['chat_id'] == chat_id) & (df['word'] == word)]
    if len(slice) == 0:
        df.loc[len(df)] = [chat_id, word, 1]

    else:
        df.loc[(df['chat_id'] == chat_id) & (df['word'] == word), 'rate'] += 1


    df.to_csv(way_to_db, index=False, encoding="utf-8-sig")
    bot.set_message_reaction(message.chat.id, message.message_id,reaction=[ReactionTypeEmoji(emoji="👌")])