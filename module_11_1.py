import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. Использование библиотеки requests
print("Запрос данных с сайта https://urban-university.ru/")

# Отправка GET-запроса

url = 'https://urban-university.ru/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Данные успешно получены:")
    print("Первые 500 символов ответа:")
    print(response.text[:500])
else:
    print("Ошибка при запросе данных:", response.status_code)


# 2. Использование библиотеки pandas
print("\nСоздание DataFrame вручную...")
data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'age': [24, 27, 22, 32, 29],
    'salary': [50000, 54000, 52000, 58000, 60000],
    'department': ['IT', 'HR', 'IT', 'Finance', 'HR']
}

df = pd.DataFrame(data)
print("Первые 5 строк данных:")
print(df.head())

print("\nФильтрация данных по определенному условию...")
filtered_df = df[df['age'] > 25]  # Фильтрация по возрасту > 25
print(filtered_df)

print("\nГруппировка данных и вычисление среднего значения...")
grouped_df = df.groupby('department')['salary'].mean()
print(grouped_df)

# 3. Использование библиотеки matplotlib
print("\nВизуализация данных...")
plt.figure(figsize=(10, 5))

# Простой график
plt.subplot(1, 2, 1)
plt.plot(df['age'], df['salary'], 'bo-')
plt.title('Возраст и Зарплата')
plt.xlabel('Возраст')
plt.ylabel('Зарплата')

# Столбчатая диаграмма
plt.subplot(1, 2, 2)
grouped_df.plot(kind='bar', color='orange', ax=plt.gca())
plt.title('Средняя зарплата по отделам')
plt.xlabel('Отдел')
plt.ylabel('Средняя зарплата')

plt.tight_layout()
plt.show()



