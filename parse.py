import requests
import csv
from bs4 import BeautifulSoup

import pprint
from config import DOMEN, URL, HEADERS, dict_marks


def get_html(url, headers=HEADERS, params=None):
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        return r.text

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='a-list__item')
    # print(items)
    data =[]
    for item in items:
        # print(item)
        try:
            title = item.find('div', class_='a-card__header').find('a').get_text(strip=True)
            description = item.find('p', class_='a-card__description').get_text(strip=True)
            description_data = description.split(',')
            year = description_data[0]
            type_car = description_data[1]
            ob = description_data[2]
            type_topliva = description_data[3]
            kpp = description_data[4]
            price = item.find('span',class_='a-card__price').get_text(strip=True)\
                      .replace('\xa0','').replace('₸','')
            city = item.find('div', class_='a-card__data').find('span', class_='a-card__param').get_text(strip=True)
            date = item.find('div', class_='a-card__data').find('span', class_='a-card__param a-card__param--date').get_text(strip=True)
            views = item.find('span', {"class": 'a-card__views'}).get_text(strip=True)
            picture = item.find('img').get('src')
            link = DOMEN + item.find('div', class_='a-card__header').find('a').get('href')
            marka = title.split(' ')[0]
            if marka in dict_marks:
                marka = dict_marks[marka]

            data.append({
                'marka': marka,
                'title': title,
                'year': year,
                'type_car': type_car,
                'ob': ob,
                'type_topliva': type_topliva,
                'kpp': kpp,
                'price': price,
                'city': city,
                'date': date,
                'views': views,
                'picture': picture,
                'link': link,

            })
        except Exception as e:
            print(e)
    return data

def save_to_csv(data):
    with open('cars.csv', 'a') as f:
        filedsnames = data[0].keys()
        writer = csv.DictWriter(f, filedsnames)
        writer.writeheader()
        writer.writerows(data)

def parser(page=1):
    contents = []
    for p in range(2, page+1):
        html = get_html(URL, params={'page': p} if p !=1 else None)
        content = get_content(html)
        contents.extend(content)
        print(f"Страница {p} спарсена")
    return contents 

# pprint.pprint(parser(5))

save_to_csv(parser(5))