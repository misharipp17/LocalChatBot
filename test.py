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

if __name__ == '__main__':
    unittest.main()
