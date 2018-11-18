def gas(said_tag):
    url = 'staticfiles/api/json/gas.json'
    with open(url) as file:
        data = json.load(file)

    infos = {'在哪': 'address', '地址': 'address', '電話': 'tel', '資訊': 'all'}

    reply = str()
    contain_kw = False
    region_dict = dict()
    for i, j in data.items():
        region_dict[i] = [element for element in j['regions']]
        
    # 尋找單一加油站
    for kw in infos:
        if kw in said_tag:
            contain_kw = True
            if kw == '在哪':
                kw = '地址'
            for city, i in data.items():
                for j in i['regions'].values():
                    for station, info in j.items():
                        if station in said_tag:
                            if kw == '資訊':
                                reply = "{station}的電話是{tel}，地址是{adr}".format(station=station, tel=info['tel'], adr=info['address'])
                            else:
                                reply = "{station}的{kind}是{ans}".format(station=station, kind=kw, ans=info[infos[kw]])
    if not reply and contain_kw:
        reply = "我們找不到您想要的資訊。可能您有錯別字或是沒有打出加油站全名？"
    elif not reply:
        for city, regions in region_dict.items():
            for region in regions:
                if region[:-1] in said_tag:
                    reply = city + region + '的加油站有'
                    ex = str()
                    for i in data[city]['regions'][region]:
                        reply += i + '、'
                        ex = i
                    reply = reply[:-1] + "你可以針對某一個加油站詢問詳細資訊。例如：'我想知道{ex}的資訊'".format(ex=ex)
        if not reply:
            for city in region_dict:
                if city in said_tag:
                    reply = city + '有'
                    for i in data[city]['regions']:
                        reply += i[:-1] + '、'
                        ex = i
                    reply = reply[:-1] + "等行政區。你可以針對某個行政區詢問有哪些加油站。例如：'{ex}有哪些加油站？'".format(ex=ex)
    return reply
