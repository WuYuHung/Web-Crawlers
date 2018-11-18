def fat(said_tag, step):
    if step == 0:
        reply"請說出查詢的食物熱量(比如:可樂的熱量,一個奶酥麵包的熱量)"
    else:
        urls = ['http://health.nkfust.edu.tw/svelte/sveltep3_{num}.htm'.format(num=i) for i in range(1, 9)]
        urls.append('http://health.nkfust.edu.tw/svelte/sveltep3.htm')
        frames = []

        for index, url in enumerate(urls):
            part_df = pd.read_html(url)[1]
            part_df = part_df.iloc[1:]
            if index == 0:
                part_df[4] = np.nan
                part_df = part_df[[0, 1, 4, 2, 3]]
            if index == 5:
                part_df[3] = part_df[4] = np.nan
                part_df = part_df[[0, 1, 3, 4, 2]]
            if index == 6:
                part_df[4] = np.nan
                part_df = part_df[[0, 1, 2, 4, 3]]
            part_df.columns = [i for i in range(5)]
            frames.append(part_df)
        df = pd.concat(frames)
        df = df.fillna('-')
        df = df.sort_values(by=[1], ascending=False)
        try:
            for food in df[1]:
                if food.split(' ')[0] in said_tag:
                    data = df[df[1] == food].values.tolist()[0][1:]
                    break
            reply = "{food}的熱量是{fat}卡！".format(
                food=data[0].replace(' ', ''), fat=data[3])
            for i in [2, 1]:
                if data[i] != '-':
                    reply = data[i] + reply
        except:
            reply = "很抱歉，我們找不到相關的資訊"

    return reply
