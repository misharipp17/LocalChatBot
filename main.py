import telebot
import psycopg2
from text import get_offset, search_directspeech, filter_lower_words, keep_alpha, capitalize_words, search_qoutation, find_with_offset

con = psycopg2.connect(
    database="books",
    user="chatbot",
    password="mrvl",
    host="127.0.0.1",
    port="5432"
)
print('success')
cur = con.cursor()
cur.execute("INSERT INTO authors (name, middlename, surname) VALUES ('0', '0', '0')")
#cur = con.cursor()
#cur.execute("SELECT * from authors")
#cur1.execute("SELECT * from books")
#rows = cur.fetchall()
#rows1 = cur1.fetchall()
#print(rows, rows1)
token = open('token.txt').read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start \n Вот какие команды я могу исполнять: \n /quotation - найти имя персонажа и главу в книге по введенной Вами цитате. \n /character - выделить как можно больше цитат персонажа в заданной главе.\n /searchbook - вывожу список книг в моей базе данных, прохождение этой команды необходимо для использования остальных команд.')

@bot.message_handler(commands=['searchbook'])
def start_quotation(message):
    global state
    state = 'searchbook'
    bot.send_message(message.chat.id, 'Вот какие авторы у меня есть:')
    #for row in rows1:
        #bot.send_message(message.chat.id, row[1] + ' ' + row[2] + ' ' + row[3])
    bot.send_message(message.chat.id, 'Есть ли среди них нужный Вам автор?(Да/Нет)')


@bot.message_handler(commands=['quotation'])
def start_quotation(message):
    global state
    state = 'quotation'
    bot.send_message(message.chat.id, 'Напишите Вашу цитату.')
    for row in rows1:
        bot.send_message(message.chat.id, row[1] + ' ' + row[2] + ' ' + row[3])
@bot.message_handler(commands=['character'])
def start_character(message):
    global state
    state = 'character'
    bot.send_message(message.chat.id, 'Напишите персонажа, и главу, и ,возможно, название книги.')

@bot.message_handler(content_types=['document'])
def handle_text_doc(message):
    global file_name
    if state == 'searchbook':
        document_id = message.document.file_id
        file_id_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        file_name = message.document.file_name
        with open('downloaded_books/' + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Я загрузил вашу книгу, можете пользоваться остальными моими командами)')
    else:
        bot.send_message(message.chat.id, 'Извините, но Вы прислали это не вовремя.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    file_name = 'example.txt'
    global state
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Напиши мне /start, чтобы узнать, что я умею.')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока, хорошего дня!')
    elif state == 'searchbook':
        if message.text.lower() == "да":
            bot.send_message(message.chat.id, 'Напишите его Имя/Фамилию/Отчество так как оно записано в сообщении выше.')
        elif message.text.lower() == "нет":
            bot.send_message(message.chat.id, 'Напишите его Имя/Фамилию/Отчество и следуюущим сообщением пришлите файл с нужной Вам книгой.')
            state = 'author'
    elif state == 'author':
        phio = message.text.lower().split()
        author = ({'name': phio[0].capitalize(), 'middlename': phio[1].capitalize(), 'surname': phio[2].capitalize()})
        cur = con.cursor()
        cur.execute("INSERT INTO authors (name, middlename, surname) VALUES ('0', '0', '0')")
        print('Yes')
    elif state == 'quotation':
        if True:
            if message.text.lower() == "да":
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBVkRfYOL4e95nsf0BQTNERFzXlRPXCQAC6AIAArVx2gZSDa62VYCCWxsE')
                bot.send_message(message.chat.id, 'Я рад, что смог Вам помочь. Есть ли еще цитаты для меня?')
            elif message.text.lower() == "нет":
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBVktfYPUL4o_PjERkI5qn7OAbxX48mQACGgADWbv8JTxSipCGVVnTGwQ')
                bot.send_message(message.chat.id, 'Попробуйте исправить цитату или прислать мне книжку')
            else:
                text = open("downloaded_books/" + file_name, encoding="utf-8").read()
                keep_alpha_line, offset_list = get_offset(text)
                lower_words = {word for word in keep_alpha_line.split() if word.islower()}
                quotation = message.text
                quotation_author = ''
                lines_with_quotation = search_qoutation(quotation, file_name)
                if len(lines_with_quotation) == 0:
                    lines_with_quotation, punct_quotations = find_with_offset(quotation, file_name)
                    if len(lines_with_quotation) == 0:
                        bot.send_message(message.chat.id, 'Цитата не найдена, дополните или исправите цитату')
                    else:
                        bot.send_message(message.chat.id, 'Вот возможные абзацы с этой цитатой и ее авторы:')
                        for k in range(len(lines_with_quotation)):
                            quotation = punct_quotations[k]
                            potential_authors = []
                            result_author, result_direct = search_directspeech(lines_with_quotation[k])
                            for i in range(len(result_direct)):
                                if result_direct[i].find(quotation) != -1:
                                    quotation_author = result_author[i]
                            capitalize_list = capitalize_words(keep_alpha(quotation_author))
                            potential_authors = filter_lower_words(capitalize_list, lower_words)
                            bot.send_message(message.chat.id, lines_with_quotation[k])
                            if len(potential_authors) != 0:
                                bot.send_message(message.chat.id, potential_authors[0])
                            else:
                                while len(potential_authors) == 0:
                                    previous_paragraph = list(open("downloaded_books/" + file_name, encoding="utf-8"))[k - 1]
                                    previous_capitalize_list = capitalize_words(keep_alpha(previous_paragraph))
                                    potential_authors = filter_lower_words(previous_capitalize_list, lower_words)
                                bot.send_message(message.chat.id, potential_authors[- 1])
                        bot.send_message(message.chat.id, 'Нашли ли Вы ответ на свой вопрос?(Да/Нет)')
                else:
                    bot.send_message(message.chat.id, 'Вот возможные абзацы с этой цитатой и ее авторы:')
                    for line in lines_with_quotation:
                        potential_authors = []
                        result_author, result_direct = search_directspeech(line)
                        for i in range(len(result_direct)):
                            if result_direct[i].find(quotation) != -1:
                                quotation_author = result_author[i]
                        capitalize_list = capitalize_words(keep_alpha(quotation_author))
                        potential_authors = filter_lower_words(capitalize_list, lower_words)
                        bot.send_message(message.chat.id, line)
                        if len(potential_authors) != 0:
                            bot.send_message(message.chat.id, potential_authors[0])
                        else:
                            while len(potential_authors) == 0:
                                previous_paragraph = list(open("downloaded_books/" + file_name, encoding="utf-8"))[
                                    list(open("downloaded_books/" + file_name, encoding="utf-8")).index(line) - 1]
                                previous_capitalize_list = capitalize_words(keep_alpha(previous_paragraph))
                                potential_authors = filter_lower_words(previous_capitalize_list, lower_words)
                            bot.send_message(message.chat.id, potential_authors[- 1])
                    bot.send_message(message.chat.id, 'Нашли ли Вы ответ на свой вопрос?(Да/Нет)')
    elif state == 'character':
        text = open('example.txt', encoding="utf-8").read()
state = ''
file_name = ''
def test():
    file_name = 'example.txt'
    text = open("downloaded_books/" + file_name, encoding="utf-8").read()
    lower_words = {word for word in keep_alpha(text).split() if word.islower()}
    quotation = 'В будущую жизнь?'
    quotation_author = ''
    print(search_qoutation(quotation, file_name))
    lines_with_quotation = search_qoutation(quotation, file_name)
    for line in lines_with_quotation:
        potential_authors = []
        result_author, result_direct = search_directspeech(line)
        for sentence in range(len(result_direct)):
            if result_direct[sentence].find(quotation) != -1:
                quotation_author = result_author[sentence]
        capitalize_list = capitalize_words(keep_alpha(quotation_author))
        potential_authors = filter_lower_words(capitalize_list, lower_words)
        try:
            print(potential_authors)
        except:
            continue

if __name__ == '__main__':
    bot.polling()
    #print(get_offset('— Ну,   хорошо'))

