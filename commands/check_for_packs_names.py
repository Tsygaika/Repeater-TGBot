import openpyxl     #ЭТОТ ФАЙЛ КАЖЕТСЯ НАДО УДАЛИТЬ

def check_for_packs_names(bot, call):
    book = openpyxl.open("data.xlsx")
    sheets_list = book.sheetnames  # получаем список листов

    for i in sheets_list:  # ищем лист беседы
        if i == str(call.message.chat.id):
            sheet = book[i]
            book.active = book[i]  # задаем новую активную страницу
            break

    if sheet[0 + 1][0 + 0].value == None:  # если есть хоть одна колода
        bot.send_message(call.message.chat.id, "<code>Ошибка №1 в файле check_for_packs_names</code>\nСообщить об ошибке @Tsygaika",
                         parse_mode='HTML')
        book.close()
        return False

    else:
        i = 0
        pack_list = []  #список с названиями колод

        while i < sheet.max_column + 1:
            pack_list.append(sheet[0 + 1][i + 0].value)
            i += 10

        book.close()

        if call.data in pack_list:
            return True

        else:
            print(call.data, pack_list)
            bot.send_message(call.message.chat.id, "<code>Ошибка №2 в файле check_for_packs_names</code>\nСообщить об ошибке @Tsygaika",
                             parse_mode='HTML')
            return False