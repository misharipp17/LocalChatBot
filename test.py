from text import get_offset, search_directspeech, filter_lower_words, keep_alpha, capitalize_words, search_qoutation
import unittest


class TextFunCheck(unittest.TestCase):
    def test_offset(self):
        self.assertEqual(get_offset('— Ну,   хорошо'), (' Ну хорошо', [1, 1, 1, 2, 4, 4, 4, 4, 4, 4]))
    
    def test_search_qoutation(self):
        quotation = 'В будущую жизнь?'
        file_name = 'example.txt'
        res = search_qoutation(quotation, file_name)
        self.assertEqual(len(res), 2)
    
    def test_offset_with_restore(self):
        example = """— Нет, отчего же вы думаете, — вдруг начал Пьер, опуская голову и принимая вид бодающегося быка, отчего вы так думаете? Вы не должны так думать."""
        quotation = 'Нет отчего - же... вы думаете'
        clear_example, offset = get_offset(example)
        clear_quotation = keep_alpha(quotation)
        clear_begin = clear_example.find(clear_quotation)
        clear_end = clear_begin + len(clear_quotation) - 1
        self.assertEqual([clear_begin + offset[clear_begin], clear_end + offset[clear_end] + 1], [2, 27])


if __name__ == '__main__':
    unittest.main()
