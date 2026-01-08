def send_long_message(bot, chat_id, text):
    while text:
        bot.send_message(chat_id, text[:4096])
        text = text[4096:]