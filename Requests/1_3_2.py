# -*- coding: UTF-8 -*-

from OutputPackage import *
import requests
import os
import json
import execjs


def Tip():
    print("（1）中文 -> 英文")
    print("（2）英文 -> 中文")


def Get_BaiduSign(x):
    with open("baidu_sign.js") as f:
        jsData = f.read()
        _sign = execjs.compile(jsData).call("e", x)
        return _sign


if __name__ == "__main__":
    Fm.Start_PG()
    # UA伪装
    UAHeaders = {
        'Cookie': "PSTM=1568970864; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=CFAF9E83FE1D358043F064134A3246AF:FG=1; BIDUPSID=A9F407DCE0E28222FDB1A94E6C20D075; BDUSS=5LVTRkem5YTXdOUy15Qk10eVJLbE1EUkY1UGVyc2pXMWxNWkZ0TS11N1dsZ0pmRVFBQUFBJCQAAAAAAAAAAAEAAAAm1XINMTE4MzEwMzAxNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANYJ217WCdtea2; BDUSS_BFESS=5LVTRkem5YTXdOUy15Qk10eVJLbE1EUkY1UGVyc2pXMWxNWkZ0TS11N1dsZ0pmRVFBQUFBJCQAAAAAAAAAAAEAAAAm1XINMTE4MzEwMzAxNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANYJ217WCdtea2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=3; H_PS_PSSID=7540_32617_1463_7567_31660_7552_32675_7631_32116_32580; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1599534248,1599899815,1599899891,1599901899; yjs_js_security_passport=bfff248833ff4eb1b64618b8c16b9f1d159cd2eb_1599902099_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1599902276; __yjsv5_shitong=1.0_7_ac0eea500bf9c43f81395593d381439efea3_300_1599902277347_112.4.142.150_4b30f4c0",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    # 指定参数
    from_lan, to_lan = "", ""
    # 用户选择翻译方式
    while True:
        print('感谢百度翻译，禁止用于商业用途')
        print('------------------------')
        Tip()
        temp = input("请选择翻译方式: ")
        if temp == '1':
            from_lan, to_lan = "zh", "en"
            break
        elif temp == '2':
            from_lan, to_lan = "en", "zh"
            break
        else:
            print("输入不合法")
            continue
    # 输入要翻译的内容
    kw = input(f"请输入要翻译的内容（{from_lan} -> {to_lan}）：")
    post_data = {
        ' from': from_lan,
        'to': to_lan,
        'query': kw,
        'simple_means_flag': '3',
        'transtype': 'translang',
        "sign": None,
        "token": "da043a07f72265bca9c899c66a25c89a"
    }
    # 获取百度sign
    sign = Get_BaiduSign(kw)
    post_data['sign'] = sign
    post_url = "https://fanyi.baidu.com/v2transapi"
    try:
        response = requests.post(url=post_url, data=post_data, headers=UAHeaders)
    except OSError as err:
        print(f"{OSError}: 请求失败")
        raise
    else:
        print("请求成功")
    # json返回一个对象，要确认响应数据为json类型
    dict_data = response.json()
    # 显示翻译结果
    print(dict_data['trans_result']['data'][0]['dst'])
    # 持久化存储
    path = os.getcwd() + f'\\Data\\{from_lan}_{to_lan}'
    fp = open(path + f'\\{from_lan}_{to_lan}_{kw}.json', 'w', encoding='utf-8')
    json.dump(dict_data, fp=fp, ensure_ascii=False)  # 中文不用ascii码
    Fm.End_PG()
