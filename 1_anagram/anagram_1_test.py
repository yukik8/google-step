import unittest
# ファイル名の先頭に数字を入れると無効なので注意
from anagram_1_1_map import find_anagram


class test_find_anagram():

    # ノーマル
    def test_normal(self):
        result = find_anagram('1_anagram/Words.txt', 'silent')
        self.assertIn('listen', result)
        self.assertIn('enlist', result)

    # anagramが複数ある場合
    def test_multiple_anagrams(self):
        result = find_anagram('1_anagram/Words.txt', 'eat')
        self.assertIn("tea", result)
        self.assertIn("ate", result)

    # anagramが見つからない場合
    def test_no_anagrams(self):
        with self.assertRaises(ValueError):
            find_anagram("ahlfhwefhuipfff", "1_anagram/Words.txt")

    # 与えられた単語がとても短い場合
    def test_short(self):
        result = find_anagram('1_anagram/Words.txt', 'y')
        self.assertIn("y", result)

    # 与えられた単語がとても長い場合
    def test_long(self):
        result = find_anagram('1_anagram/Words.txt', 'revolutionizes')
        self.assertIn("revolutionizes", result)

    # 空の文字列が与えられたとき
    def test_empty(self):
        with self.assertRaises(ValueError):
            find_anagram('1_anagram/Words.txt', '')
