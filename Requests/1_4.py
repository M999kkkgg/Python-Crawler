# -*- coding: UTF-8 -*-

from OutputPackage import *
import requests
import os
import json
import pandas as pd


# 返回种类名以及代号
def Select_Type(**TypeDict):
    Keys = list(TypeDict.keys())
    print("排行榜中的电影种类如下:")
    for i in range(len(Keys)):
        print(f"\t{Keys[i]}", end="")
        if (i+1) % 3 == 0:
            Fm.Newline()
        else:
            continue
    x = None
    while True:
        if x not in Type_dict:
            x = input("请选择你要筛选的种类: ")
        else:
            y = Type_dict[x]
            break
    return x, y


if __name__ == "__main__":
    Fm.Start_PG()
    # url
    url = "https://movie.douban.com/j/chart/top_list"
    # UA
    UAHeaders = {
        "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Cookie": "bid=7iZSKgfo-4c; douban-fav-remind=1; trc_cookie_storage=taboola%2520global%253Auser-id%3D27934956-07bc-4572-9a63-2ea7f197f02d-tuct49c998b; __yadk_uid=770F4Wo56PWMpDcoTCRnreLAv073vHzL; ll=\"118159\"; gr_user_id=4a266a86-ac97-4ab9-84bf-6a8f6b627fd8; __gads=ID=303e495512b5c0b5:T=1582949647:S=ALNI_MZlGzt3033LUttjmS0FOr2T3sfrSw; _vwo_uuid_v2=D646E891FB1F2E89C134814A3EEE85706|a6d698fca4f8325c9df9d8ef14bc9b76; viewed=\"26606389_26860166_27199642_4180711_30626642_33408247_27116331_24257229\"; __utmz=223695111.1585985228.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=30149280.1599482082.8.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1599921077%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D9_4Uojg1ql4ypPRFzwwWo3u9YFstlWk3KGA_tcpBxSFA0vC5pZxO4WX-OT0kj3WC2dTVtE75-XJ3SxC768cVhq%26wd%3D%26eqid%3Dec721ce40004005a000000025e8836c7%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1762547439.1573993861.1599482082.1599921078.9; __utmb=30149280.0.10.1599921078; __utmc=30149280; __utma=223695111.813398203.1573993861.1585985228.1599921078.5; __utmb=223695111.0.10.1599921078; __utmc=223695111; _pk_id.100001.4cf6=56949ba4375f56eb.1573993861.5.1599921224.1585985228."
    }
    # 设置参数-1
    Interval_id = "100:90"
    Action = ""
    Start = "0"
    Limit = "100"
    Type_dict = {'喜剧': '24', '剧情': '11', '动作': '5', '爱情': '13', '科幻': '17', '动画': '25',
                 '悬疑': '10', '战争': '22', '历史': '4', '冒险': '15', '儿童': '8', '奇幻': '16'}
    # 用户选择筛选种类
    TName, Type = Select_Type(**Type_dict)
    # 用户自定义开始位置以及筛选数目
    print(f"默认的开始位置以及筛选数目: ({Start},{Limit})")
    Start = input("请输入开始检索的位置: ")
    Limit = input("请输入你要筛选的数目: ")
    # 设置参数-2
    param = {
        'type': Type,
        'interval_id': Interval_id,
        'action': Action,
        'start': Start,
        'limit': Limit
    }
    # 保存数据JSON
    response = requests.get(url=url, params=param, headers=UAHeaders)
    list_data = response.json()
    path = os.getcwd() + '\\Data\\Douban\\JSON'
    file_name = f"{TName}_{Start}_{Limit}.json"
    path = path + f"\\{file_name}"
    with open(path, 'w', encoding='utf-8') as fp:
        json.dump(list_data, fp, ensure_ascii=False, indent=4)
    print("搜集完毕")
    # 保存数据CSV
    Columns = ['排名', '片名', '评分', '上映时间', '国家', '演员']
    num = len(list_data)
    df_data = pd.DataFrame({
        '排名': [list_data[i]['rank'] for i in range(num)],
        '片名': [list_data[i]['title'] for i in range(num)],
        '评分': [list_data[i]['score'] for i in range(num)],
        '上映时间': [list_data[i]['release_date'] for i in range(num)],
        '国家': [list_data[i]['regions'] for i in range(num)],
        '演员': [list_data[i]['actors'] for i in range(num)],
    }, columns=Columns)
    path_csv = os.getcwd() + '\\Data\\Douban\\CSV'
    csv_name = f"{TName}_{Start}_{Limit}.csv"
    path_csv = path_csv + f"\\{csv_name}"
    df_data.to_csv(path_csv, 'a', encoding='UTF-8', index=False)
    Fm.End_PG()
