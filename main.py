import telebot

token = open('token.txt').read()
bot = telebot.TeleBot(token)
state = ''
quotation = ''
character = ''
print(state)
def search_qoutation(quotation, file_name): 
    """получает цитату и файл с книжкой, возвращает список абзацев с данной цитатой"""
    paragraph = []
    for line in open(file_name, encoding="utf-8"):
        number_quotation = line.lower().find(quotation.lower())
        if number_quotation != -1:
            paragraph.append(line)
    return paragraph
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
        text = open('war-peace.txt', encoding="utf-8").read()
        #print(text.lower().find(message.text.lower()))
    elif state == 'character':
        character = message
        text = open('war-peace.txt', encoding="utf-8").read()
if __name__ == '__main__':
    quotation = 'до свидания'
    print(search_qoutation(quotation, 'war-peace.txt'))
#bot.polling()
