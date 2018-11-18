def brain_storm(said_tag, step, variable):
    if step == 0:
        re = requests.get('http://proxy.yphs.tp.edu.tw/~ypi/hpclasssample/6information/6_4_01.htm')
        re.encoding = 'utf-8'
        soup = BeautifulSoup(re.text, "lxml")
        soup_all = soup.find_all('p')
        while True:
            n = random.choice([i for i in range(2, len(soup_all) - 1, 2)])
            q = a = ""
            try:
                string = str(soup_all[n])
                li = string.split('<br/>')
                seperate = li[1].split('答案：')
                q = seperate[0].split('—')[1]
                q.replace('</p>', '')
                a = seperate[1].replace('</p>', '').strip()
                break
            except:
                continue
        reply = q
    else:
        reply = "哈哈！！答案是：" + variable['answer']
    return reply
