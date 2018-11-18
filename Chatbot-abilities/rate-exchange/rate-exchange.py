def exchange_rate(said_tag, step):
    if step == 0:
        response = Reply('coin', "請說出您想查詢的幣值?(比如:1000台幣換日幣,台幣對美元的匯率)", step=step, nstep=step+1)
    else:
        kw_dict = {'臺': 19, '台': 19, '美': 0, '港': 1, '英': 2, '澳': 3, '拿': 4, '新': 5, '士': 6, '法': 6, '日': 7, '非': 8, '典': 9, '紐': 10,
                   '泰': 11, '菲': 12, '尼': 13, '歐': 14, '韓': 15, '越': 16, '馬': 17, '人': 18}
        number_dict = {'零': 0, '一': 1, '二': 2, '兩': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                       '十': 10,'百': 10 ** 2 ,'千': 10 ** 3, '萬': 10 ** 4, '億': 10 ** 8}
        kw_info_dict = {}
        df = pd.read_html('https://rate.bot.com.tw/xrt?Lang=zh-TW')[0]
        rate_list = df['現金匯率']['本行賣出'].tolist()
        rate_list.append(1)
        innum = False
        isChineseNum = False
        for word in said_tag:
            if word in number_dict:
                if isChineseNum:
                    kw_info_dict['value'] += word
                else:
                    kw_info_dict['value'] = word
                    kw_info_dict['value_index'] = said_tag.index(word)
                    isChineseNum = True
            if word.isnumeric() or word == '.':
                if innum:
                    kw_info_dict['value'] += word
                else:
                    kw_info_dict['value'] = word
                    kw_info_dict['value_index'] = said_tag.index(word)
                    innum = True
            if word in kw_dict:
                if 'kind1' not in kw_info_dict:
                    kw_info_dict['kind1'] = word
                    kw_info_dict['kind1_index'] = said_tag.index(word)
                else:
                    kw_info_dict['kind2'] = word
                    kw_info_dict['kind2_index'] = said_tag.index(word)
        if isChineseNum:
            kw_info_dict['value'] = tk_help.convertChineseToNum(kw_info_dict['value'])
        if 'value' not in kw_info_dict:
            result = float(rate_list[kw_dict[kw_info_dict['kind1']]]) / float(rate_list[kw_dict[kw_info_dict['kind2']]])
        elif abs(int(kw_info_dict['kind2_index']) - int(kw_info_dict['value_index'])) > abs(int(kw_info_dict['kind1_index']) - int(kw_info_dict['value_index'])):
            result = float(kw_info_dict['value']) * float(
                rate_list[kw_dict[kw_info_dict['kind1']]]) / float(rate_list[kw_dict[kw_info_dict['kind2']]])
        else:
            result = float(kw_info_dict['value']) * float(
                rate_list[kw_dict[kw_info_dict['kind2']]]) / float(rate_list[kw_dict[kw_info_dict['kind1']]])
        reply = '大約是' + str(round(result,2)))
    return reply
