import requests
from bs4 import BeautifulSoup

def generate_soup(url):
    re = requests.get(url)
    re.encoding = 'big5'
    soup = BeautifulSoup(re.text, 'lxml')
    return soup

BASIC_URL = 'https://www2.moeaboe.gov.tw/oil102/oil2017/map/'

said_tag = "新北有哪裡可以加油??"

location_dict = dict()

# generate information

said_tag.replace('臺', '台')

tw_soup = generate_soup(BASIC_URL + 'taiwan.asp')
for i in tw_soup.findAll('area', href=True):
    city_soup = generate_soup(BASIC_URL + i['href'])
    location_dict[city_soup.find('title').text] = {'url': i['href']}
    location_dict[city_soup.find('title').text]['regions'] = dict()
print(location_dict)
for key, value in location_dict.items():
    city_soup = generate_soup(BASIC_URL + value['url'])
    for c in city_soup.findAll('area', href=True):
        region_soup = generate_soup(BASIC_URL + c['href'])
        location_dict[key]['regions'][region_soup.findAll('td')[1].text[3:6]] = c['href']
print(location_dict)
