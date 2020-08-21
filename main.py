import telebot

token = open('token.txt').read()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start \n Вот какие команды я могу исполнять: \n /quotation - найти имя персонажа и главу в книге по введенной Вами цитате. \n /character - выделить как можно больше цитат персонажа в заданной главе.')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет! Как я могу Вам помочь?')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока, хорошего дня!')

@bot.message_handler(commands=['quotation'])
def send_character(message):
    bot.send_message(message.chat.id, 'Напишите Вашу цитату и возможно название книги.')

bot.polling()
