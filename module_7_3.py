class WordsFinder:
    def __init__(self, *file_names):
        self.file_names = file_names

    def get_all_words(self):
        all_words = {}
        for file_name in self.file_names:
            with open(file_name, 'r', encoding='utf-8') as file:
                line = file.read().lower()
                for punctuation in [',', '.', '=', '!', '?', ';', ':', ' - ']:
                    line = line.replace(punctuation, '')
                words = line.split()
                all_words[file_name] = words
        return all_words

    def find(self, word):
        result = {}
        for name, words in self.get_all_words().items():
            if word.lower() in words:
                result[name] = words.index(word.lower()) + 1
        return result

    def count(self, word):
        result = {}
        for name, words in self.get_all_words().items():
            result[name] = words.count(word.lower())+1
        return result

finder2 = WordsFinder('test_file.txt')
print(finder2.get_all_words()) # Все слова
print(finder2.find('TEXT')) # 3 слово по счёту
print(finder2.count('teXT')) # 4 слова teXT в тексте всего
