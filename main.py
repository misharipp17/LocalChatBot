from text import get_offset, search_directspeech, filter_lower_words, keep_alpha, capitalize_words, search_qoutation
from bot import bot


if __name__ == '__main__':
    bot.polling()
    print(get_offset('— Ну,   хорошо'))

