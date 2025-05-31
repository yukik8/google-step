import unittest
# ファイル名の先頭に数字を入れると無効なので注意
from anagram_1_map import find_anagram


class test_find_anagram(unittest.TestCase):

    # ノーマル
    def test_normal(self):
        result = find_anagram('data/words.txt', 'silent')
        self.assertIn('listen', result)
        self.assertIn('enlist', result)

    # anagramが複数ある場合
    def test_multiple_anagrams(self):
        result = find_anagram('data/words.txt', 'eat')
        self.assertIn("tea", result)
        self.assertIn("ate", result)

    # anagramが見つからない場合
    def test_no_anagrams(self):
        with self.assertRaises(ValueError):
            find_anagram('data/words.txt', 'ahlfhwefhuipfff')

    # 与えられた単語がとても短い場合
    def test_short(self):
        result = find_anagram('data/words.txt', 'y')
        self.assertIn("y", result)

    # 与えられた単語がとても長い場合
    def test_long(self):
        result = find_anagram('data/words.txt', 'revolutionizes')
        self.assertIn("revolutionizes", result)

    # 空の文字列が与えられたとき
    def test_empty(self):
        with self.assertRaises(ValueError):
            find_anagram('data/words.txt', '')


if __name__ == '__main__':
    unittest.main()
