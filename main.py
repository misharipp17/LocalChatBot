import telebot

def filter_lower_words(capitalize_list, lower_words):
    """Возращает только те слова из capitalize_list, которых в маленьком регистве нет среди lower_words"""
    return {word for word in capitalize_list if word.lower() not in lower_words}

def keep_alpha(line):
    return ''.join(c if c.isalpha() else ' ' for c in line)

def capitalize_words(line):
    """Возвращает список заглавных слов из строки line, в которой нет знаков пунктуации, длиной больше 1 буквы."""
    return {word for word in line.split() if word == word.capitalize() and len(word) > 1}

def search_qoutation(quotation, file_name):
    """получает цитату и файл с книжкой, возвращает список абзацев с данной цитатой"""
    paragraph = []
    for line in open(file_name, encoding="utf-8"):
        number_quotation = line.lower().find(quotation.lower())
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
    bot.send_message(message.chat.id, 'Напишите Вашу цитату и, возможно, название книги.')

@bot.message_handler(commands=['character'])
def start_character(message):
    global state
    state = 'character'
    bot.send_message(message.chat.id, 'Напишите персонажа, и главу, и ,возможно, название книги.')

@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    if state == 'quotation':
        document_id = message.document.file_id
        file_id_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        paragraphs = search_qoutation(qoutation, src)
    
    else:
        bot.send_message(message.chat.id, 'Извините, но Вы прислали это не вовремя.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Как я могу Вам помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока, хорошего дня!')
    elif state == 'quotation':
        quotation = message
        text = open('example.txt', encoding="utf-8").read()
        #print(text.lower().find(message.text.lower()))
    elif state == 'character':
        character = message
        text = open('example.txt', encoding="utf-8").read()

state = ''
character = ''

def test():
    file_name = 'example.txt'
    text = open(file_name, encoding="utf-8").read()
    lower_words = {word for word in keep_alpha(text).split() if word.islower()}
    quotation = 'Что́ я думаю? я слушал тебя.'
    print(search_qoutation(quotation, file_name))
    for line in search_qoutation(quotation, file_name):
        capitalize_list = capitalize_words(keep_alpha(line))
        print(capitalize_list - filter_lower_words(capitalize_list, lower_words), capitalize_list, filter_lower_words(capitalize_list, lower_words))

if __name__ == '__main__':
    #bot.polling()
    test()
