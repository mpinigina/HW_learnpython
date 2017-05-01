import vk
import json
from time import sleep
import matplotlib.pyplot as plt
from requests.exceptions import ReadTimeout
from collections import defaultdict
from datetime import datetime, date


def get_all_posts(domain):
    response = api.wall.get(domain='space', count=100)
    posts_count = response['count']
    all_posts = response['items']
    for offset in range(len(all_posts), posts_count, 100):
        response = api.wall.get(domain='space', count=100, offset=offset)
        all_posts += response['items']
    return posts_count, all_posts


def get_all_comments(all_posts):
    for post in all_posts:
        response = api.wall.getComments(owner_id=post['owner_id'], post_id=post['id'], count=100)
        comments_count = response['count']
        post['comments'] = response['items']
        for offset in range(len(post['comments']), comments_count, 100):
            response = api.wall.getComments(owner_id=post['owner_id'], post_id=post['id'], count=100)
            post['comments'] += response['items']
    return all_posts


def calculate_average_text_lengths(all_posts):
    for post in all_posts:
        post_text = post['text'].split(' ')
        post_text = [word for word in post_text if word]
        post['post_len'] = len(post_text)
        comments_length_sum = 0
        for comment in post['comments']:
            comment_text = comment['text'].split(' ')
            comment_text = [word for word in comment_text if word and (word.isdigit() or word.isalpha())]
            comment['comment_len'] = len(comment_text)
            comments_length_sum += len(comment_text)
        post['comments_len_avg'] = comments_length_sum / len(post['comments'])
    return all_posts


def calculate_age(bdate):
    today = date.today()
    bdate = datetime.strptime(bdate, '%d.%m.%Y').date()
    age = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
    return age


def get_user_city_and_age(all_posts):
    for post in all_posts:
        for comment in post['comments']:
            try:
                user_info = api.users.get(user_ids=comment['from_id'], fields='bdate,city')[0]
            except ReadTimeout:
                user_info = {}
            comment['city'] = user_info.get('city', {})
            comment['city_title'] = comment['city'].get('title', 'Не указан')
            comment['city'] = comment['city'].get('id', -1)
            bdate = user_info.get('bdate', 'Не указан')
            if bdate != 'Не указан' and len(bdate.split('.')) == 3:
                comment['age'] = calculate_age(bdate)


def aggregate_comments_by_attribute(all_comments, attribute):
    comments_by_attribute = defaultdict(list)
    for comment in all_comments:
        comments_by_attribute[comment.get(attribute)].append(comment)
    return comments_by_attribute


def calculate_average_comment_len(aggregated_comments):
    for attribute, comments in aggregated_comments.items():
        comments_lens = [comment['comment_len'] for comment in comments]
        aggregated_comments[attribute] = sum(comments_lens) / len(comments_lens)
    aggregated_comments[-1] = comments_by_age.pop(None)
    return aggregated_comments


def plot_data(x, y=None, xlabel=None, ylabel=None, legend=None, plot_type='plot'):
    plot_type = getattr(plt, plot_type)
    if x and y:
        chart = plt.plot(x, y)
    else:
        chart = plt.plot(x)
    chart.xlabel(xlabel)
    chart.ylabel(ylabel)
    chart.legend(legend)
    chart.show()


if __name__ == '__main__':
    session = vk.Session()
    api = vk.API(session, v='5.63')
    posts_count, all_posts = get_all_posts(domain='space')
    print('Количество постов в сообществе ВКосмосе - ' + str(posts_count))
    all_posts = [{'id': post['id'], 'owner_id': post['owner_id'], 'text': post['text']} for post in all_posts]
    all_posts = get_all_comments(all_posts)
    all_posts = calculate_average_text_lengths(all_posts)
    all_posts = get_user_city_and_age(all_posts)
    all_comments = []

    for post in all_posts:
        all_comments += post['comments']

    comments_by_age = aggregate_comments_by_attribute(all_comments, 'age')
    comments_by_city = aggregate_comments_by_attribute(all_comments, 'city')
    avg_comments_by_age = calculate_average_comment_len(comments_by_age)
    avg_comments_by_city = calculate_average_comment_len(comments_by_city)
    points = sorted([(post['post_len'], post['comments_len_avg']) for post in all_posts])
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    plot_data(x, y, xlabel='x = номер поста', ylabel='y = средняя длина в словах')
    plot_data(points, legend=['Номер поста', 'Длина поста'])
    plot_data(list(avg_comments_by_age.items()), legend=['Возраст коментатора', 'Длина комментария'])

    # Все возраста после 70-ти - скорее всего фейковые
    plot_data(list(avg_comments_by_age.keys()),
              list(avg_comments_by_age.values()),
              xlabel='x = возраст',
              ylabel='y = длина поста в словах',
              plot_type='bar')

    # Нормируем id городов, чтобы получился нормальный график
    cities_ids = list(avg_comments_by_city.keys())
    points = [(x - min(cities_ids)) / (max(cities_ids) - min(cities_ids)) for x in cities_ids]
    plot_data(points,
              list(avg_comments_by_city.values()),
              xlabel='x = id города',
              ylabel='y = длина поста в словах',
              plot_type='bar')
