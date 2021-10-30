import requests
import os
from string import punctuation
from bs4 import BeautifulSoup


def create_file_name(folder, filename):
    result = ''
    for i in filename:
        if i in punctuation:
            continue
        elif i == ' ':
            result += '_'
        else:
            result += i
    return os.path.join(folder, result + '.txt')


def article_body(link):
    url = 'https://www.nature.com' + link
    r2 = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup2 = BeautifulSoup(r2.content, 'html.parser')
    content = soup2.find('div', {'class': 'c-article-body'}).text
    return content


number_of_pages = int(input())
article_type = input()

for i in range(1, number_of_pages + 1):
    folder = f'Page_{i}'
    url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}'
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    code = r.status_code
    if code == 200:
        if not os.access(folder, os.F_OK):
            os.mkdir(folder)
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            type = article.find('span', class_="c-meta__type").text
            if type == article_type:
                file_name = create_file_name(folder, article.a.text)
                content_link = article.find('a', {'data-track-action': "view article"}).get('href')
                content = article_body(content_link)
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(content)
print('Saved all articles.')
