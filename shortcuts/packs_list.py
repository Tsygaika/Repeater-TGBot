#используется только тогда, когда есть хотя бы одна колода
import openpyxl

def packs_list(bot, message):
    book = openpyxl.open("data/data.xlsx")
    sheets_list = book.sheetnames  # получаем список листов

    for i in sheets_list:  # ищем лист беседы
        if i == str(message.chat.id):
            sheet = book[i]
            book.active = book[i]  # задаем новую активную страницу
            break

    else:   #если не создан лист, возвращаем ошибку
        bot.send_message(message.chat.id, "<code>Ошибка №8 в файле packs_list</code>\nСообщить об ошибке @Tsygaika",
                         parse_mode='HTML')

    i = 0
    array = []
    if sheet[0 + 1][0 + 0].value != None:  # если есть хоть одна колода

        while i < sheet.max_column + 1:  # создаем кнопки с названием каждой колоды
            array.append(sheet[0 + 1][i + 0].value)
            i += 10

    #если нет колод, значит он создает только первую колоду

    return array