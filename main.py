import telebot

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

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Как я могу Вам помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока, хорошего дня!')
    elif message1 == 'quotation':
        text = open('token.txt', encoding="utf-8").read()
        print(text.lower().find(message.text.lower()))
    elif message1 == 'character':
        bot.send_message(message.chat.id, 'Персонаж')
bot.polling()
