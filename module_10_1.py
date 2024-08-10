from time import sleep
from datetime import datetime
from threading import Thread

time_start = datetime.now()


def wite_words(word_count, file_name):
    with open(file_name, 'w') as file:
        for word in range(1, word_count + 1):
            file.write(f"Какое-то слово № {word} \n")
            sleep(0.1)

    print(f"Завершилась запись в файл {file_name}")
    pass


time_start = datetime.now()

wite_words(10, "example1.txt")
wite_words(30, 'example2.txt')
wite_words(200, 'example3.txt')
wite_words(100, 'example4.txt')

time_and = datetime.now()
time_result = time_and - time_start
print(f'Работа потоков {time_result}')

time_start = datetime.now()

wite_words_1 = Thread(target=wite_words, args=(10, "example5.txt"))
wite_words_2 = Thread(target=wite_words, args=(30, "example6.txt"))
wite_words_3 = Thread(target=wite_words, args=(200, "example7.txt"))
wite_words_4 = Thread(target=wite_words, args=(100, "example8.txt"))

wite_words_1.start()
wite_words_2.start()
wite_words_3.start()
wite_words_4.start()

wite_words_1.join()
wite_words_2.join()
wite_words_3.join()
wite_words_4.join()

time_and = datetime.now()
time_result = time_and - time_start
print(f'Работа потоков {time_result}')
