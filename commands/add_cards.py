import openpyxl

def add_cards(bot, message):
    book = openpyxl.open("data/data.xlsx")
    sheets_list = book.sheetnames  # получаем список листов

    for i in sheets_list:  # ищем лист беседы
        if i == str(message.chat.id):
            sheet = book[i]
            book.active = book[i]  # задаем новую активную страницу
            break

    else:  # если листа для такой беседы нет, то создаем
        book.create_sheet(str(message.chat.id))
        book.active = book[str(message.chat.id)]
        sheet = book.active

    book.save('data/data.xlsx')  # сохраняем

    from commands.packs_list import packs_list
    packs_list(bot, message, sheet)  # вывели сообщение с колодами
    book.close()