import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://auto.ria.com/newauto/marka-jaguar/'
HEADER = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0','accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADER, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    puslapiavimas = soup.find_all('span', class_='mhide')
    if puslapiavimas:
        return int (puslapiavimas[-1].get_text())
    else:
        return 1
    print(puslapiavimas)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars =[]
    for item in items:
        uah_price = item.find('span', class_='grey size13')
        if uah_price:
            uah_price = uah_price.get_text()
        else:
            uah_price = 'Del kainos kreipkitės'
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'Link': HOST + item.find('a').get('href'),
            'USD': item.find('span', class_='green').get_text(),
            'uah_price': uah_price,
            'city': item.find('svg', class_='svg svg-i16_pin').find_next('strong').get_text()
        })
    return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Automobilio pavadinimas', 'Nuoroda', 'Kaina USD', 'Kaina UAH', 'Automobilis yra mieste'])
        for item in items:
            writer.writerow([item['title'], item['Link'], item['USD'], item['uah_price'], item['city']])

def parse():
    URL = input('Nurodykite URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Svetainės parsingas {page} iš {pages_count}...')
            html = get_html(URL, params={'page':page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)

        print(f'Gauta {len(cars)} automobilių')
    else:
        print('Klaida')


parse()