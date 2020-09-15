from text import get_offset, search_directspeech, filter_lower_words, keep_alpha, capitalize_words, search_qoutation
from bot import bot

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
    print(get_offset('— Ну,   хорошо'))

