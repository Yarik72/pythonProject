from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import xlsxwriter
from tabulate import tabulate
import time
import random


# Функция для задержки с случайной продолжительностью
def random_delay(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))


# Функция для скроллинга страницы
def scroll_to_bottom(page):
    try:
        page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
        random_delay(0.8, 0.9)  # Подождите, чтобы страница загрузилась
    except Exception as e:
        print(f"Ошибка при прокрутке страницы: {e}")


# Открываем все телефоны
def open_phone_numbers_for_all_cards(page):
    land_plots = page.locator('div[data-testid="object_card"]')
    card_count = land_plots.count()

    for index in range(card_count):
        try:
            card_locator = land_plots.nth(index)
            phone_button = card_locator.locator('button[data-testid="show_phone_card_desktop"]')
            phone_button.scroll_into_view_if_needed()
            phone_button.click()
            random_delay(0.8, 0.9)
        except Exception as e:
            print(f"Ошибка при нажатии на кнопку 'Показать телефон' для карточки {index + 1}: {e}")


# Парсинг страницы
def parse_page(page):
    page_content = page.content()
    soup = BeautifulSoup(page_content, 'html.parser')

    land_plots = soup.find_all('div', {'data-testid': 'object_card'})
    grouped_plots = {}

    def extract_base_address(address):
        # Возвращаем часть адреса до первой запятой, если она есть
        if "," in address:
            return address.split(",")[0].strip()
        return address.strip()

    for plot in land_plots:
        title_div = plot.find('div', class_='mW0Ci')
        title = title_div.find_all('span')[0].text.strip() if title_div else 'Не указан'
        area = title_div.find_all('span')[2].text.strip() if title_div else 'Не указана'

        # Обработка площади в сотках
        try:
            area = round(float(area.split()[0]), 1)  # Округляем до одного знака после запятой
        except ValueError:
            area = 0

        try:
            price = plot.find('span', class_='eypL8 uwvkD').text.strip().replace("руб.", "").replace(" ", "")
            price = int(price)
        except AttributeError:
            price = 0

        try:
            address = plot.find('div', class_='EDAsp').text.strip()
            base_address = extract_base_address(address)
        except AttributeError:
            address = 'Не указан'
            base_address = 'Не указан'

        try:
            link = plot.find('a', href=True)['href']
            full_url = f"https://www.etagi.com{link}"
        except TypeError:
            full_url = 'Не указана'

        try:
            phone_number = plot.find('button', {'data-testid': 'phone_number_realtor_object_card'}).text.strip()
            realtor_name = plot.find('span', class_='qVZET').text.strip()
        except AttributeError:
            phone_number = 'Не указан'
            realtor_name = 'Не указан'

        if base_address not in grouped_plots:
            grouped_plots[base_address] = []

        grouped_plots[base_address].append({
            "Заголовок": title,
            "Площадь": area,
            "Цена": price,
            "Адрес": address,
            "Ссылка": full_url,
            "Телефон": phone_number,
            "Имя": realtor_name
        })

    for base_address, plots in grouped_plots.items():
        grouped_plots[base_address] = sorted(plots, key=lambda x: x['Цена'])

    return grouped_plots


# Функция для форматирования валюты
def format_currency(value):
    return f"{value:,}".replace(",", " ")


# Сохранение данных в CSV и Excel
def save_to_files(all_grouped_plots):
    csv_file = "../Все участки.csv"
    min_max_csv_file = "../мин_макс_цена.csv"
    min_max_xlsx_file = "../мин_макс_цена"
    workbook = xlsxwriter.Workbook('../Все участки.xlsx')
    worksheet = workbook.add_worksheet()

    # Заголовки для Excel
    worksheet.write(0, 0, "Заголовок")
    worksheet.write(0, 1, "Площадь")
    worksheet.write(0, 2, "Цена")
    worksheet.write(0, 3, "Адрес")
    worksheet.write(0, 4, "Ссылка")
    worksheet.write(0, 5, "Телефон")
    worksheet.write(0, 6, "Имя")

    # Сохранение данных в CSV
    with open(csv_file, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for address, plots in all_grouped_plots.items():
            for plot in plots:
                writer.writerow([
                    plot["Заголовок"],
                    plot["Площадь"],
                    plot["Цена"],
                    plot["Адрес"],
                    plot["Ссылка"],
                    plot["Телефон"],
                    plot["Имя"]
                ])

    # Сохранение данных в Excel
    row = 1
    for address, plots in all_grouped_plots.items():
        for plot in plots:
            worksheet.write(row, 0, plot["Заголовок"])
            worksheet.write(row, 1, plot["Площадь"])
            worksheet.write(row, 2, plot["Цена"])
            worksheet.write(row, 3, plot["Адрес"])
            worksheet.write(row, 4, plot["Ссылка"])
            worksheet.write(row, 5, plot["Телефон"])
            worksheet.write(row, 6, plot["Имя"])
            row += 1

    workbook.close()

    # Сохранение данных для min_max в CSV и Excel
    min_max_data = []
    for base_address, plots in all_grouped_plots.items():
        if not plots:
            continue

        prices_by_area = {}
        for plot in plots:
            area_key = f"{int(plot['Площадь'])}"
            if area_key not in prices_by_area:
                prices_by_area[area_key] = {
                    "Мин. цена": plot['Цена'],
                    "Ссылка мин.": plot['Ссылка'],
                    "Телефон мин.": plot['Телефон'],
                    "Имя мин.": plot['Имя'],
                    "Макс. цена": plot['Цена'],
                    "Ссылка макс.": plot['Ссылка'],
                    "Телефон макс.": plot['Телефон'],
                    "Имя макс.": plot['Имя']
                }
            else:
                if plot['Цена'] < prices_by_area[area_key]['Мин. цена']:
                    prices_by_area[area_key]['Мин. цена'] = plot['Цена']
                    prices_by_area[area_key]['Ссылка мин.'] = plot['Ссылка']
                    prices_by_area[area_key]['Телефон мин.'] = plot['Телефон']
                    prices_by_area[area_key]['Имя мин.'] = plot['Имя']
                if plot['Цена'] > prices_by_area[area_key]['Макс. цена']:
                    prices_by_area[area_key]['Макс. цена'] = plot['Цена']
                    prices_by_area[area_key]['Ссылка макс.'] = plot['Ссылка']
                    prices_by_area[area_key]['Телефон макс.'] = plot['Телефон']
                    prices_by_area[area_key]['Имя макс.'] = plot['Имя']

        for area, details in prices_by_area.items():
            row = [base_address, area,
                   format_currency(details['Мин. цена']),
                   details['Ссылка мин.'], details['Телефон мин.'], details['Имя мин.'],
                   format_currency(details['Макс. цена']),
                   details['Ссылка макс.'], details['Телефон макс.'], details['Имя макс.']]
            min_max_data.append(row)

    # Сохранение данных для min_max в CSV
    with open(min_max_csv_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Базовый адрес", "Площадь",
            "Мин. цена", "Ссылка (мин. цена)", "Телефон (мин. цена)", "Имя (мин. цена)",
            "Макс. цена", "Ссылка (макс. цена)", "Телефон (макс. цена)", "Имя (макс. цена)"
        ])
        writer.writerows(min_max_data)

    # Сохранение данных для min_max в Excel
    min_max_workbook = xlsxwriter.Workbook(min_max_xlsx_file)
    min_max_worksheet = min_max_workbook.add_worksheet()

    min_max_worksheet.write(0, 0, "Базовый адрес")
    min_max_worksheet.write(0, 1, "Площадь")
    min_max_worksheet.write(0, 2, "Мин. цена")
    min_max_worksheet.write(0, 3, "Ссылка (мин. цена)")
    min_max_worksheet.write(0, 4, "Телефон (мин. цена)")
    min_max_worksheet.write(0, 5, "Имя (мин. цена)")
    min_max_worksheet.write(0, 6, "Макс. цена")
    min_max_worksheet.write(0, 7, "Ссылка (макс. цена)")
    min_max_worksheet.write(0, 8, "Телефон (макс. цена)")
    min_max_worksheet.write(0, 9, "Имя (макс. цена)")

    row = 1
    for row_data in min_max_data:
        min_max_worksheet.write_row(row, 0, row_data)
        row += 1

    min_max_workbook.close()


# Вывод данных в консоль в виде таблицы
def print_final_table(all_grouped_plots):
    table_data = []

    for base_address, plots in all_grouped_plots.items():
        if not plots:
            continue

        prices_by_area = {}
        for plot in plots:
            area_key = f"{int(plot['Площадь'])}"
            if area_key not in prices_by_area:
                prices_by_area[area_key] = {
                    "Мин. цена": plot['Цена'],
                    "Ссылка мин.": plot['Ссылка'],
                    "Телефон мин.": plot['Телефон'],
                    "Имя мин.": plot['Имя'],
                    "Макс. цена": plot['Цена'],
                    "Ссылка макс.": plot['Ссылка'],
                    "Телефон макс.": plot['Телефон'],
                    "Имя макс.": plot['Имя']
                }
            else:
                if plot['Цена'] < prices_by_area[area_key]['Мин. цена']:
                    prices_by_area[area_key]['Мин. цена'] = plot['Цена']
                    prices_by_area[area_key]['Ссылка мин.'] = plot['Ссылка']
                    prices_by_area[area_key]['Телефон мин.'] = plot['Телефон']
                    prices_by_area[area_key]['Имя мин.'] = plot['Имя']
                if plot['Цена'] > prices_by_area[area_key]['Макс. цена']:
                    prices_by_area[area_key]['Макс. цена'] = plot['Цена']
                    prices_by_area[area_key]['Ссылка макс.'] = plot['Ссылка']
                    prices_by_area[area_key]['Телефон макс.'] = plot['Телефон']
                    prices_by_area[area_key]['Имя макс.'] = plot['Имя']

        for area, details in prices_by_area.items():
            row = [base_address, area,
                   format_currency(details['Мин. цена']),
                   details['Ссылка мин.'], details['Телефон мин.'], details['Имя мин.'],
                   format_currency(details['Макс. цена']),
                   details['Ссылка макс.'], details['Телефон макс.'], details['Имя макс.']]
            table_data.append(row)

    print(tabulate(table_data, headers=[
        "Базовый адрес", "Площадь,сот.",
        "Мин. цена,руб.", "Ссылка (мин. цена)", "Телефон (мин. цена)", "Имя (мин. цена)",
        "Макс. цена,руб.", "Ссылка (макс. цена)", "Телефон (макс. цена)", "Имя (макс. цена)"
    ], tablefmt="simple_grid"))


# Основной скрипт
def main(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # random_delay(1.0, 1.2)

        all_grouped_plots = {}
        page_number = 1

        while True:
            print(f"Парсинг страницы {page_number}")

            # Прокрутка и открытие телефонов
            scroll_to_bottom(page)
            open_phone_numbers_for_all_cards(page)

            # Парсинг данных с текущей страницы
            page_data = parse_page(page)
            for address, plots in page_data.items():
                if address not in all_grouped_plots:
                    all_grouped_plots[address] = []
                all_grouped_plots[address].extend(plots)

            # Переход на следующую страницу
            next_button = page.locator("button:has-text('Следующая')")
            if next_button.is_visible():
                print(f"Переход на следующую страницу")
                next_button.click()
                random_delay(0.8, 0.9)  # Подождите, пока загрузится новая страница
                page_number += 1
            else:
                print("Больше нет страниц для перехода.")
                break

        # Сохранение данных в файлы
        save_to_files(all_grouped_plots)

        # Вывод результатов в консоль
        print_final_table(all_grouped_plots)

        browser.close()


# Запуск основного скрипта
if __name__ == "__main__":
    import datetime
    start = datetime.datetime.now()
    url = 'https://www.etagi.com/realty_out/?type[]=12&area_land_min=9&area_land_max=15&district_id[]=9306&district_id[]=8868&district_id[]=8864&district_id[]=8865&district_id[]=8875&district_id[]=8877'
    # url = 'https://www.etagi.com/realty_out/?type[]=12'
    # url = 'https://www.etagi.com/realty_out/?type[]=12&area_land_min=9&area_land_max=12'
    main(url)
    end = datetime.datetime.now()
    print(end-start)