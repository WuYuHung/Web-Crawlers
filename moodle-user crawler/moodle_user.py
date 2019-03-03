# author: 吳昱宏
# title: Moodle user crawler
# created at: May 13, 2018
# last modified at: March 3, 2019

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

class_id = str(input('請輸入您想查詢的課程代碼或關鍵字：').upper())

soup = BeautifulSoup(html_post.text, 'html.parser')

classes = list() # 不用dict的原因為下面操作會較不方便
for i in soup.find_all('a', href=True):
    if class_id in str(i.string):
        classes.append([i.string, i['href']])

if len(classes) == 0:
    print('您的輸入有誤，或是權限不足！！（若您無選修該堂課，無法查詢）')
else:
    if len(classes) == 1:
        class_name, class_url = classes[0][0], classes[0][1]
    else:
        output_str = ''.join(['{}. {}\n'.format(str(index + 1), i[0]) for index, i in enumerate(classes)])
        try:
            index = int(input('查到多筆課程，請用數字回答你要搜尋哪一堂課：\n' + output_str))
        except:
            print('輸入有誤！')
        if index > len(classes):
            print('輸入有誤！')
        else:
            class_name, class_url = classes[index - 1][0], classes[index - 1][1]
    print('查詢課程：' + class_name)
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