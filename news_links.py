import urllib.request
# библиотеки для работы с датой
from datetime import datetime, timedelta
import re
import os
# подключение файла mark_news.py
import mark_news

# главная страница сайта
main_page = 'http://tumentoday.ru'
# номер выгруженной статьи
file_id = 0

# преобразование переменной даты в строку
# в формате год/месяц/день
def date_to_url(date):
    return datetime.strftime(date, '%Y/%m/%d')

# получение html-страницы по ее адресу
def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        result = page.read().decode('utf8')
    except:
        result = ''
    return result

def mark_news_by_date(date):
    # получаем доступ к глобальной переменной
    global file_id
    # links - все ссылки на статьи на текущий день
    links = []
    # номер страницы для текущей даты
    page_id = 1
    while True:
        # формирование ссылки на страницу архива
        page_url = '%s/%s/?page=%d' % (main_page, date_to_url(date), page_id)
        # попытка получения страницы
        page = download_page(page_url)
        # если нет страницы, то выходим из цикла
        if page == '':
            break;
        # извлечение ссылок на новости за текущий день
        reg = ('<div class="item">.*?<div class="title">.*?<a href="'+
               '(/%s.*?)">.*?</a>.*?</div>.*?</div>' % (date_to_url(date)))
        regNewsLinks = re.compile(reg, flags=re.DOTALL)
        # все ссылки на статьи на текущий день на данной странице
        page_links = regNewsLinks.findall(page)
        # добавление ссылок на новости с текущей страницы к предыдущим
        links.extend(page_links)
        # выводит адрес страницы архива и кол-во найденных статей
        print('%s. %d found' % (page_url, len(page_links)))
        # переход к следующей странице
        page_id += 1
    # удаление повторяющихся ссылок
    # links переводится в тип "множество", дубликаты
    # автоматически удаляются, после чего переводим обратно в массив
    links = list(set(links))
    for link in links:
        file_id += 1
        mark_news.mark_page(link, file_id)

def mark_all_news():
    first_date = datetime(2009, 3, 21)
    last_date = datetime.now()
    # кол-во дней между первой и последней датами
    day_amount = (last_date - first_date).days
    for day in range(0, day_amount + 1):
        new_date = first_date + timedelta(days=day)
        mark_news_by_date(new_date)
