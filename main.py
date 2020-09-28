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
con1 = psycopg2.connect(
    database="authors",
    user="chatbot",
    password="mrvl",
    host="127.0.0.1",
    port="5432"
)
cur1 = con1.cursor()
cur = con.cursor()
rows = cur.fetchall()
rows1 = cur1.fetchall()
print("Yes")
token = open('token.txt').read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '������, �� ������� ��� /start \n ��� ����� ������� � ���� ���������: \n /quotation - ����� ��� ��������� � ����� � ����� �� ��������� ���� ������. \n /character - �������� ��� ����� ������ ����� ��������� � �������� �����.\n /searchbook - ������ ������ ���� � ���� ���� ������, ����������� ���� ������� ���������� ��� ������������� ��������� ������.')

@bot.message_handler(commands=['quotation'])
def start_quotation(message):
    global state
    state = 'searchbook'
    bot.send_message(message.chat.id, '��� ����� ������ � ���� ����:')
    bot.send_message(message.chat.id, '���� �� ����� ��� ������ ��� �����?(��/���)')
    for row in rows1:
        bot.send_message(message.chat.id, row[1] + ' ' + row[2] + ' ' + row[3])


@bot.message_handler(commands=['quotation'])
def start_quotation(message):
    global state
    state = 'quotation'
    bot.send_message(message.chat.id, '�������� ���� ������.')
    for row in rows1:
        bot.send_message(message.chat.id, row[1] + ' ' + row[2] + ' ' + row[3])
@bot.message_handler(commands=['character'])
def start_character(message):
    global state
    state = 'character'
    bot.send_message(message.chat.id, '�������� ���������, � �����, � ,��������, �������� �����.')

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
        bot.send_message(message.chat.id, '� �������� ���� �����, ������ ������������ ���������� ����� ���������)')
    else:
        bot.send_message(message.chat.id, '��������, �� �� �������� ��� �� �������.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    global state
    if message.text.lower() == '������':
        bot.send_message(message.chat.id, '������! ������ ��� /start, ����� ������, ��� � ����.')
    elif message.text.lower() == '����':
        bot.send_message(message.chat.id, '����, �������� ���!')
    elif state == 'searchbook':
        if message.text.lower() == "��":
            bot.send_message(message.chat.id, '�������� ��� ���/�������/�������� ��� ��� ��� �������� � ��������� ����.')
        elif message.text.lower() == "���":
            bot.send_message(message.chat.id, '�������� ��� ���/�������/�������� � ���������� ���������� �������� ���� � ������ ��� ������.')
            state = 'author'
    elif state == 'author':
        author = message.text.lower.split()
        cur.execute("INSERT INTO STUDENT (name, surname, middlename) VALUES (%(author[0]), %(author[1]), %(author[2]))", author)
    elif state == 'quotation':
        if True:
            if message.text.lower() == "��":
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBVkRfYOL4e95nsf0BQTNERFzXlRPXCQAC6AIAArVx2gZSDa62VYCCWxsE')
                bot.send_message(message.chat.id, '� ���, ��� ���� ��� ������. ���� �� ��� ������ ��� ����?')
            elif message.text.lower() == "���":
                bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBVktfYPUL4o_PjERkI5qn7OAbxX48mQACGgADWbv8JTxSipCGVVnTGwQ')
                bot.send_message(message.chat.id, '���������� ��������� ������ ��� �������� ��� ������')
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
                        bot.send_message(message.chat.id, '������ �� �������, ��������� ��� ��������� ������')
                    else:
                        bot.send_message(message.chat.id, '��� ��������� ������ � ���� ������� � �� ������:')
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
                        bot.send_message(message.chat.id, '����� �� �� ����� �� ���� ������?(��/���)')
                else:
                    bot.send_message(message.chat.id, '��� ��������� ������ � ���� ������� � �� ������:')
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
                    bot.send_message(message.chat.id, '����� �� �� ����� �� ���� ������?(��/���)')
    elif state == 'character':
        text = open('example.txt', encoding="utf-8").read()
state = ''
file_name = ''
def test():
    file_name = 'example.txt'
    text = open("downloaded_books/" + file_name, encoding="utf-8").read()
    lower_words = {word for word in keep_alpha(text).split() if word.islower()}
    quotation = '� ������� �����?'
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
    #print(get_offset('� ��,   ������'))

