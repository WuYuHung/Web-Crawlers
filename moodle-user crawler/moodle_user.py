import requests
import getpass
import sys
from lxml import html
from bs4 import BeautifulSoup

# should not modify
session = requests.Session()
USER = input('請輸入Moodle帳號：')
PASSWORD = getpass.getpass('請輸入密碼：')
LOGIN_URL = 'https://moodle.ntust.edu.tw/login/'

# get token
try:
    result = session.get(LOGIN_URL, timeout=3)
except requests.exceptions.ReadTimeout:
    print('連線超時，可能是學校Moodle的server掛了或者你的連線品質太差！(當前timeout設定：3 seconds)')
    sys.exit()
tree = html.fromstring(result.text)
logintoken = list(set(tree.xpath('//input[@name="logintoken"]/@value')))[0]

post_data = {'username': USER, 'password': PASSWORD, 'logintoken': logintoken}

html_post = session.post(LOGIN_URL, post_data)

class_id = str(input('請問您想查詢的課程代碼是：').upper())

soup = BeautifulSoup(html_post.text, 'html.parser')

for i in soup.find_all('a', href=True):
    if class_id in str(i.string):
        print("查詢課程：" , i.string)
        class_url = i['href']

try: 
    class_url = class_url.replace("course", "user")
    class_url = class_url.replace("view", "index")
    class_url += "&perpage=5000"

    new_request = session.post(class_url, post_data)
    soup = BeautifulSoup(new_request.text, 'html.parser')
    user_list = list()
    for i in soup.find_all('a'):
        if '@ ' in str(i.string) and '老師' not in str(i.string):
            user_list.append(i.string.replace('@', ' '))
    user_list.sort()
    print('包含助教共計 {length} 人'.format(length=len(user_list)))
    print(*user_list, sep = '\n')
except:
    print('您的輸入有誤，或是權限不足！！（若您無選修該堂課，無法查詢）')