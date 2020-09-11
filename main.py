import telebot
import re

def get_offset(text):
    """Возвращает список смещений, которые возникают из-за удаления из строки знаков пунктуации, для каждого символа и саму строку только из букв и одинарных пробелов.
    offset('— Ну,   хорошо') -> ' Ну хорошо', [1, 1, 1, 2, 4, 4, 4, 4, 4, 4]"""
    result = []
    line_result = ''
    offset = 0
    for i in range(len(text)):
        if text[i].isalpha() or (text[i] == ' ' and (i == 0 or text[i - 1] != ' ')):
            result.append(offset)
            line_result += text[i]
        else:
            offset += 1
    return line_result, result
def search_directspeech(line):
    """Возвращает прямую речь из абзаца."""
    word = r'\b\w+\b'
    word_punct = word + r'\S?'
    sentence = word_punct + r'(?:\s*' + word_punct + ')*'
    direct = sentence
    author = sentence
    end = '[.?!]'
    comma_end = '[.?!,]'
    template_author0 = direct + '—' + '(' + author + ')' + end
    template_author1 = '(' + author + ')' + ":" + direct + end
    template_author2 = direct + '—' + '(' + author + ')' + comma_end + '—' + direct
    template_author3 = '— ' + direct + ' — ' + '(' + author + ')' + end
    template_author4 = '— ' + direct + ' — ' + author + comma_end + ' — ' + '(' + direct + ')' + ' — ' + '(' + author + ')' + end
    template_direct0 = '(' + direct + ')' + '—' + author + end
    template_direct1 =author + ":" + '(' + direct + ')' + end
    template_direct2 = '(' + direct + ')' + '—' + author + comma_end + '—' + direct
    template_direct3 = '— ' + '(' + direct + ')' + ' — ' + author + end
    template_direct4 = '— ' + '(' + direct + ')' + ' — ' + author + comma_end + ' — ' +'(' + direct + ')' + ' — ' + author + end
    '''ошибка с кортежем'''
    result_author = re.findall(template_author3, line) + re.findall(template_author2, line) + re.findall(template_author1, line) + re.findall(template_author0, line) + re.findall(template_author4, line)
    result_direct = re.findall(template_direct3, line) + re.findall(template_direct2, line) + re.findall(template_direct1, line) + re.findall(template_direct0, line) + re.findall(template_direct4, line)
    return result_author, result_direct

def filter_lower_words(capitalize_list, lower_words):
    """Возращает только те слова из capitalize_list, которых в маленьком регистве нет среди lower_words."""
    return [word for word in capitalize_list if word.lower() not in lower_words]

def keep_alpha(line):
    line = line.translate(str.maketrans('','',chr(769)))
    line = ''.join(c if c.isalpha() else ' ' for c in line)
    while '  ' in line:
        line = line.replace('  ', ' ')
    return line

def capitalize_words(line):
    """Возвращает список заглавных слов из строки line, в которой нет знаков пунктуации, длиной больше 1 буквы."""
    return [word for word in line.split() if word == word.capitalize() and len(word) > 1]

def search_qoutation(quotation, file_name):
    """Получает цитату и файл с книжкой, возвращает список абзацев с данной цитатой."""
    paragraph = []
    for line in open(file_name, encoding="utf-8"):
        number_quotation = line.lower().find(str(quotation).lower())
        if number_quotation != -1:
            paragraph.append(line)
    return paragraph

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
    else:
        bot.send_message(message.chat.id, 'Извините, но Вы прислали это не вовремя.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Как я могу Вам помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока, хорошего дня!')
    elif state == 'quotation':
        bot.send_message(message.chat.id, 'Вот возможные абзацы с этой цитатой и ее авторы:')
        file_name = 'example.txt'
        text = open(file_name, encoding="utf-8").read()
        lower_words = {word for word in keep_alpha(text).split() if word.islower()}
        quotation = message.text
        quotation_author = ''
        lines_with_quotation = search_qoutation(quotation, file_name)
        if len(lines_with_quotation) == 0:
            bot.send_message(message.chat.id, 'Цитата не найдена, дополните или исправите цитату')
        for line in lines_with_quotation:
            potential_authors = []
            result_author, result_direct = search_directspeech(line)
            for sentence in range(len(result_direct)):
                if result_direct[sentence].find(quotation) != -1:
                    quotation_author = result_author[sentence]
            capitalize_list = capitalize_words(keep_alpha(quotation_author))
            potential_authors =filter_lower_words(capitalize_list, lower_words)
            bot.send_message(message.chat.id, line)
            if len(potential_authors) != 0:
                bot.send_message(message.chat.id, potential_authors[0])
            else:
                while len(potential_authors) == 0:
                    previous_paragraph = list(open(file_name, encoding="utf-8"))[list(open(file_name, encoding="utf-8")).index(line) - 1]
                    previous_capitalize_list = capitalize_words(keep_alpha(previous_paragraph))
                    potential_authors = filter_lower_words(previous_capitalize_list, lower_words)
                bot.send_message(message.chat.id, potential_authors[- 1])
        bot.send_message(message.chat.id, 'Есть ли еще цитаты для меня?')
    elif state == 'character':
        text = open('example.txt', encoding="utf-8").read()

state = ''
character = ''

def test():
    file_name = 'example.txt'
    text = open(file_name, encoding="utf-8").read()
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
    #bot.polling()
    print(get_offset('— Ну,   хорошо'))

