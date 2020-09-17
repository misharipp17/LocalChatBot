import re

def find_with_offset(quotation, file_name):
    text = open("downloaded_books/" + file_name, encoding="utf-8")
    lines_with_quotation = []
    punct_quotations = []
    for line in text:
        clear_example, offset = get_offset(line)
        clear_quotation = keep_alpha(quotation)
        if clear_example.find(clear_quotation) != -1:
            clear_begin = clear_example.find(clear_quotation)
            clear_end = clear_begin + len(clear_quotation) - 1
            quotation = line[clear_begin + offset[clear_begin]:clear_end + offset[clear_end] + 1]
            if quotation not in punct_quotations:
                punct_quotations.append(quotation)
            lines_with_quotation.append(line)
    return lines_with_quotation, punct_quotations
def get_offset(text):
    """Возвращает список смещений, которые возникают из-за удаления из строки знаков пунктуации, для каждого символа и саму строку только из букв и одинарных пробелов.
    get_offset('— Ну,   хорошо') -> ' Ну хорошо', [1, 1, 1, 2, 4, 4, 4, 4, 4, 4]"""
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
    #template_author4 = '— ' + direct + ' — ' + author + comma_end + ' — ' + '(' + direct + ')' + ' — ' + '(' + author + ')' + end
    template_direct0 = '(' + direct + ')' + '—' + author + end
    template_direct1 =author + ":" + '(' + direct + ')' + end
    template_direct2 = '(' + direct + ')' + '—' + author + comma_end + '—' + direct
    template_direct3 = '— ' + '(' + direct + ')' + ' — ' + author + end
    #template_direct4 = '— ' + '(' + direct + ')' + ' — ' + author + comma_end + ' — ' +'(' + direct + ')' + ' — ' + author + end
    result_author = re.findall(template_author3, line) + re.findall(template_author2, line) + re.findall(template_author1, line) + re.findall(template_author0, line)
    result_direct = re.findall(template_direct3, line) + re.findall(template_direct2, line) + re.findall(template_direct1, line) + re.findall(template_direct0, line)
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
    with open('downloaded_books/' + file_name, encoding="utf-8") as f:
        for line in f:
            number_quotation = line.lower().find(str(quotation).lower())
            if number_quotation != -1:
                paragraph.append(line)
    return paragraph

