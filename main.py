import telebot
import urllib.request

token = open('token.txt').read()
bot = telebot.TeleBot(token)
message1 = ''
print(message1)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start \n Вот какие команды я могу исполнять: \n /quotation - найти имя персонажа и главу в книге по введенной Вами цитате. \n /character - выделить как можно больше цитат персонажа в заданной главе.')

@bot.message_handler(commands=['quotation'])
def start_quotation(message):
    global message1
    message1 = 'quotation'
    bot.send_message(message.chat.id, 'Напишите Вашу цитату и, возможно, название книги.')

@bot.message_handler(commands=['character'])
def start_character(message):
    global message1
    message1 = 'character'
    bot.send_message(message.chat.id, 'Напишите персонажа, и главу, и ,возможно, название книги.')

@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    if message1 == 'quotation':
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        src = massage.document.file_name
        with open('C:\Users\misha\PycharmProjects\QuotationChatBot' + "\" + src, 'wb') as new_file:
            new_file.write(downloaded_file)    
        #text = open('war-peace.txt', encoding="utf-8").read()
    #elif message1 == 'character':
    
    else:
        bot.send_message(message.chat.id, 'Извините, но Вы прислали это не вовремя.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Как я могу Вам помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока, хорошего дня!')
    elif message1 == 'quotation':
        text = open('war-peace.txt', encoding="utf-8").read()
        #print(text.lower().find(message.text.lower()))
    elif message1 == 'character':
        text = open('war-peace.txt', encoding="utf-8").read()
bot.polling()
