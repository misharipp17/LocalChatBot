import telebot
import psycopg2
from text import get_offset, search_directspeech, filter_lower_words, keep_alpha, capitalize_words, search_qoutation, find_with_offset

con = psycopg2.connect(
    database="books",
    user="chatbot",
    password="mrvl",
    host="127.0.0.1"
)
cur = con.cursor()
cur1 = con.cursor()
cur.execute("SELECT * from books")
cur1.execute("SELECT * from authors")
rows = cur.fetchall()
rows1 = cur1.fetchall()
print(rows, rows1)

token = open('token.txt').read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '��иве�, �� напи�ал мне /start \n �о� какие команд� � мог� и�полн���: \n /quotation - най�и им� пе��онажа и глав� в книге по введенной �ами �и�а�е. \n /character - в�дели�� как можно бол��е �и�а� пе��онажа в заданной главе.\n/searchbook - в�вож� �пи�ок книг в моей базе данн��, п�о�ождение ��ой команд� необ�одимо дл� и�пол�зовани� о��ал�н�� команд.')

@bot.message_handler(commands=['quotation'])
def start_quotation(message):
    global state
    state = 'searchbook'
    bot.send_message(message.chat.id, '�о� какие ав�о�� � мен� е���:')
    bot.send_message(message.chat.id, '���� ли ��еди ни� н�жн�й �ам ав�о�?(�а/�е�)')
    for row in rows1:
        bot.send_message(message.chat.id, row[1] + ' ' + row[2] + ' ' + row[3])


@bot.message_handler(commands=['quotation'])
def start_quotation(message):
    global state
    state = 'quotation'
    bot.send_message(message.chat.id, '�апи�и�е �а�� �и�а��.')
    for row in rows1:
        bot.send_message(message.chat.id, row[1] + ' ' + row[2] + ' ' + row[3])
@bot.message_handler(commands=['character'])
def start_character(message):
    global state
    state = 'character'
    bot.send_message(message.chat.id, '�апи�и�е пе��онажа, и глав�, и ,возможно, название книги.')

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
        bot.send_message(message.chat.id, 'Я заг��зил ва�� книг�, може�е пол�зова���� о��ал�н�ми моими командами)')
    else:
        bot.send_message(message.chat.id, '�звини�е, но �� п�и�лали ��о не вов�ем�.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    file_name = 'example.txt'
    global state
    if message.text.lower() == 'п�иве�':
        bot.send_message(message.chat.id, '��иве�! �апи�и мне /start, ��об� �зна��, ��о � �ме�.')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, '�ока, �о�о�его дн�!')
    elif state == 'searchbook':
        if message.text.lower() == "да":
            bot.send_message(message.chat.id, '�апи�и�е его �м�/Фамили�/���е��во �ак как оно запи�ано в �ооб�ении в��е.')
        elif message.text.lower() == "не�":
            bot.send_message(message.chat.id, '�апи�и�е его �м�/Фамили�/���е��во и �лед����им �ооб�ением п�и�ли�е �айл � н�жной �ам книгой.')
            state = 'author'
    elif state == 'author':
        author = message.text.lower.split()
        cur.execute("INSERT INTO authors (name, surname, middlename) VALUES (%(author[0]), %(author[1]), %(author[2]))", author)
    elif state == 'quotation':
        if True:
            if message.text.lower() == "да":
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBVkRfYOL4e95nsf0BQTNERFzXlRPXCQAC6AIAArVx2gZSDa62VYCCWxsE')
                bot.send_message(message.chat.id, 'Я �ад, ��о �мог �ам помо��. ���� ли е�е �и�а�� дл� мен�?')
            elif message.text.lower() == "не�":
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBVktfYPUL4o_PjERkI5qn7OAbxX48mQACGgADWbv8JTxSipCGVVnTGwQ')
                bot.send_message(message.chat.id, '�оп�об�й�е и�п�ави�� �и�а�� или п�и�ла�� мне книжк�')
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
                        bot.send_message(message.chat.id, 'Ци�а�а не найдена, дополни�е или и�п�ави�е �и�а��')
                    else:
                        bot.send_message(message.chat.id, '�о� возможн�е абза�� � ��ой �и�а�ой и ее ав�о��:')
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
                        bot.send_message(message.chat.id, '�а�ли ли �� о�ве� на �вой воп�о�?(�а/�е�)')
                else:
                    bot.send_message(message.chat.id, '�о� возможн�е абза�� � ��ой �и�а�ой и ее ав�о��:')
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
                    bot.send_message(message.chat.id, '�а�ли ли �� о�ве� на �вой воп�о�?(�а/�е�)')
    elif state == 'character':
        text = open('example.txt', encoding="utf-8").read()
state = ''
file_name = ''
def test():
    file_name = 'example.txt'
    text = open("downloaded_books/" + file_name, encoding="utf-8").read()
    lower_words = {word for word in keep_alpha(text).split() if word.islower()}
    quotation = '� б�д���� жизн�?'
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
    #print(get_offset('� ��,   �о�о�о'))))

