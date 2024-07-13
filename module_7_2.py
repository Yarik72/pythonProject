def custom_write(file_name, strings):
    strings_positions = {}
    file = open(file_name, 'w', encoding='utf-8')

    line_num = 1
    for string in strings:
        byte_position = file.tell()
        file.write(string + '\n')
        strings_positions[(line_num, byte_position)] = string
        line_num += 1

    file.close()
    return strings_positions

# Пример выполняемого кода:
info = [
    'Text for tell.',
    'Используйте кодировку utf-8.',
    'Because there are 2 languages!',
    'Спасибо!'
    ]

result = custom_write('test.txt', info)
for elem in result.items():
  print(elem)






