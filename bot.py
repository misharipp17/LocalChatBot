import telebot


token = open('token.txt').read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start \n Вот какие команды я могу исполнять: \n /quotation - найти имя персонажа и главу в книге по введенной Вами цитате. \n /character - выделить как можно больше цитат персонажа в заданной главе.')

@bot.message_handler(commands=['quotation'])
def start_quotation(message):
    global state
    state = 'quotation'
    bot.send_message(message.chat.id, 'Напишите Вашу цитату и, возможно, название книги. Вводите цитату со как в оригинале(со знаками препинания и заглавными буквами)')

@bot.message_handler(commands=['character'])
def start_character(message):
    global state
    state = 'character'
    bot.send_message(message.chat.id, 'Напишите персонажа, и главу, и ,возможно, название книги.')

@bot.message_handler(content_types=['document'])
def handle_text_doc(message):
    if state == 'quotation':
        document_id = message.document.file_id
        file_id_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        file_name = message.document.file_name
        with open('downloaded_books/' + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Я загрузил вашу книгу, можете снова прислать Вашу цитату.')
    else:
        bot.send_message(message.chat.id, 'Извините, но Вы прислали это не вовремя.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Как я могу Вам помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока, хорошего дня!')
    elif state == 'quotation':
        file_name = 'example.txt'
        try:
            if message.text.lower() == "да":
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBVkRfYOL4e95nsf0BQTNERFzXlRPXCQAC6AIAArVx2gZSDa62VYCCWxsE')
                bot.send_message(message.chat.id, 'Я рад, что смог Вам помочь. Есть ли еще цитаты для меня?')

            else:
                text = open("downloaded_books/" + file_name, encoding="utf-8").read()
                keep_alpha_line, offset_list = get_offset(text)
                lower_words = {word for word in keep_alpha_line.split() if word.islower()}
                quotation = message.text
                quotation_author = ''
                lines_with_quotation = search_qoutation(quotation, file_name)
                if len(lines_with_quotation) == 0:
                    bot.send_message(message.chat.id, 'Цитата не найдена, дополните или исправите цитату')
                else:
                    bot.send_message(message.chat.id, 'Вот возможные абзацы с этой цитатой и ее авторы:')
                    for line in lines_with_quotation:
                        potential_authors = []
                        result_author, result_direct = search_directspeech(line)
                        for sentence in range(len(result_direct)):
                            if result_direct[sentence].find(quotation) != -1:
                                quotation_author = result_author[sentence]
                        capitalize_list = capitalize_words(keep_alpha(quotation_author))
                        potential_authors = filter_lower_words(capitalize_list, lower_words)
                        bot.send_message(message.chat.id, line)
                        if len(potential_authors) != 0:
                            bot.send_message(message.chat.id, potential_authors[0])
                        else:
                            while len(potential_authors) == 0:
                                previous_paragraph = list(open("downloaded_books/" + file_name, encoding="utf-8"))[
                                    list(open(file_name, encoding="utf-8")).index(line) - 1]
                                previous_capitalize_list = capitalize_words(keep_alpha(previous_paragraph))
                                potential_authors = filter_lower_words(previous_capitalize_list, lower_words)
                            bot.send_message(message.chat.id, potential_authors[- 1])
                    bot.send_message(message.chat.id, 'Нашли ли Вы ответ на свой вопрос?(Да/Нет)')

        except:
            bot.send_message(message.chat.id, 'У меня нет этой книги, пришлите пожалуйста файл с ней.')
    elif state == 'character':
        text = open('example.txt', encoding="utf-8").read()

