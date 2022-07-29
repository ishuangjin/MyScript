import re
import sys
import traceback

import requests


def chuli_e(e):
    info = sys.exc_info()
    files = "file:{}--》lieno:{}--》function:{}--》text:{}"
    yichang_list = [str(e)]
    for file, lieno, function, text in traceback.extract_tb(info[2]):
        file1 = files.format(file, lieno, function, text)
        yichang_list.append(file1)
    yichang_text = ''.join(yichang_list)
    return yichang_text


def get_shengcheng(token, serverId, toOpenid):
    pass


def get_open_id(openid, content_id, event_type, Cookie):
    # url = f'https://game.weixin.qq.com/cqi-bin/gamecenterwap/getsmobahighlightmomentdetail?\
    # event_type={event_type}&target_openid={openid}&content_id={content_id}&method=GET\
    # &needLogin =true&abtest_cookie=AwABAAoACwAUAAMAI5ceAFeZHgCLmR4AAAA%3D&wx_header=1\
    # &pass_ticket=nuCK3W3vwtOWvVplRrxH1J1WKTXPONV7gw5f%2BeoxGvvz5rXiYPGaF198wkt45a%2BR\
    # &uin=MTQxMjYxODYzNA%3D%3D\
    # &key=0b2f2dce50123632c8561e9390553a666f207fb4f01d91806bfc0b37791142051b586c1b1e7d96d1e8b1903928fe3950e1e731ba4771406e211632bd4f8c8e460e19a07552dac60a47928834a32a6aed38ddd09c59c3a55ce5cbb7f7dff04e1ad333fa6a0e6ba6bdc74b33b01d0dc517e4b23a280d2a794d5deff5a3aa625a59'
    url = f'https://game.weixin.qq.com/cqi-bin/gamecenterwap/getsmobahighlightmomentdetail?event_type={event_type}&target_openid={openid}&content_id={content_id}&method=GET&needLogin =true&abtest_cookie=&abt=&build_version=2022032111&pass_ticket=zOzwQwUkdsFwhn9vChIZhDetyxXA45TqwZS7%2BJ7yzphVXb7eoxr9wg1AaDJ%2BC3EU&uin=MTQxMjYxODYzNA%3D%3D&key=5e6d38340dec3db44d1cf179f3d68e1f69a1c7fd9e73e4f45e810963813bd402f00fb787c94e3cd87b1cf0247941b5666dd26858ac182a3ecb2f16869e614b474d04e580071a0adba01e14f932a81e4da735484d6131e5c3ba3e1699482d85f70489a402b18a927b17b4d93d3a49b54285d4824d96bf611bfae9748193c9422d&QB&'
    payload = {}
    # headers = {
    #     'Host': 'game.weixin.qq.com',
    #     'Accept': '*/*',
    #     'Connection': 'keep-alive',
    #     'Cookie': Cookie,
    #     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.18(0x1800123f) NetType/4G Language/zh_CN WKGameHttpScheme/1',
    #     'Accept-Language': 'zh-cn',
    #     'Referer': 'https://game.weixin.qq.com/cgi-bin/h5/static/highlight-moment/index.html\
    #     ?openid=owanlspBQakzVEPRK3PMOKuKAd8g\
    #     &content_id=PDo9lnb4KOUcBMXcIdMkuCQT6V6vROxu45I0Pd0H93o\
    #     &event_type=promotioneventtype',
    #     'Accept-Encoding': 'gzip,deflate,br'
    # }
    headers = {
        'Cookie': Cookie,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Connection': 'keep-alive',
        'Host': 'game.weixin.qq.com',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63060012)',
        'Referer': 'https://game.weixin.qq.com/cgi-bin/h5/static/highlight-moment/index.html?openid=owanlskn3-DCpZnhRUWgApywOZd0&content_id=efkAJCm88tIf_KiRmh0U0g0ABW7nvOsKjDkz38PXpiY&event_type=promotioneventtype&abt=&ssid=10208&rpt_allpath=10208&wechat_pkgid=highlight_moment_index&key=5e6d38340dec3db44d1cf179f3d68e1f69a1c7fd9e73e4f45e810963813bd402f00fb787c94e3cd87b1cf0247941b5666dd26858ac182a3ecb2f16869e614b474d04e580071a0adba01e14f932a81e4da735484d6131e5c3ba3e1699482d85f70489a402b18a927b17b4d93d3a49b54285d4824d96bf611bfae9748193c9422d&uin=MTQxMjYxODYzNA%3D%3D&pass_ticket=zOzwQwUkdsFwhn9vChIZhDetyxXA45TqwZS7%2BJ7yzphVXb7eoxr9wg1AaDJ%2BC3EU'
    }
    resp_dict = requests.request("GET", url, headers=headers, data=payload).json()
    data = resp_dict.get('data')
    print(data)
    if data:
        smoba_promotion_event_detail = data.get("smoba_promotion_event_detail")
        if smoba_promotion_event_detail:
            continue_win_event = smoba_promotion_event_detail.get("continue_win_event")
            continue_win_event1 = smoba_promotion_event_detail.get('lift_star_event')
            continue_win_event2 = smoba_promotion_event_detail.get('lbs_event')
            continue_win_event3 = smoba_promotion_event_detail.get('promotion_event_detail')
            continue_win_event4 = smoba_promotion_event_detail.get('multi_kill_event')
            data_list = []

            if continue_win_event:
                key_point_battle_list = continue_win_event.get("key_point_battle_list")
                print("key_point_battle_list", key_point_battle_list)
                if key_point_battle_list:
                    for i in key_point_battle_list:
                        battle_video_url = i.get('battle_video_url')
                        game_seq_re = re.search('game_seq=(.*?)&', battle_video_url)
                        relaySvrID_re = re.search('relay_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID_re = re.search('game_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID = gameSvrID_re.group(1)
                        relaySvrID = relaySvrID_re.group(1)
                        gameseq = game_seq_re.group(1)
                        data_list.append({"gameSvrID": gameSvrID, "relaySvrID": relaySvrID, "gameseq": gameseq})
                    print('对局数', len(data_list))
            if continue_win_event1:
                key_point_battle_list = continue_win_event1.get("key_point_battle_list")
                print("key_point_battle_list", key_point_battle_list)
                if key_point_battle_list:
                    for i in key_point_battle_list:
                        battle_video_url = i.get('battle_video_url')
                        game_seq_re = re.search('game_seq=(.*?)&', battle_video_url)
                        relaySvrID_re = re.search('relay_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID_re = re.search('game_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID = gameSvrID_re.group(1)
                        relaySvrID = relaySvrID_re.group(1)
                        gameSeq = game_seq_re.group(1)
                        data_list.append({"gameSvrID": gameSvrID, "relaySvrID": relaySvrID, "gameseq": gameSeq})
                    print('对局数', len(data_list))
            if continue_win_event2:
                key_point_battle_list = continue_win_event2.get("key_point_battle_list")
                print("key_point_battle_list", key_point_battle_list)
                if key_point_battle_list:
                    for i in key_point_battle_list:
                        battle_video_url = i.get('battle_video_url')
                        game_seq_re = re.search('game_seq=(.*?)&', battle_video_url)
                        relaySvrID_re = re.search('relay_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID_re = re.search('game_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID = gameSvrID_re.group(1)
                        relaySvrID = relaySvrID_re.group(1)
                        gameSeq = game_seq_re.group(1)
                        data_list.append({"gameSvrID": gameSvrID, "relaySvrID": relaySvrID, "gameseq": gameSeq})
                    print('对局数', len(data_list))
            if continue_win_event3:
                key_point_battle_list = continue_win_event3.get("key_point_battle_list")
                print("key_point_battle_list", key_point_battle_list)
                if key_point_battle_list:
                    for i in key_point_battle_list:
                        battle_video_url = i.get('battle_video_url')
                        game_seq_re = re.search('game_seq=(.*?)&', battle_video_url)
                        relaySvrID_re = re.search('relay_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID_re = re.search('game_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID = gameSvrID_re.group(1)
                        relaySvrID = relaySvrID_re.group(1)
                        gameSeq = game_seq_re.group(1)
                        data_list.append({"gameSvrID": gameSvrID, "relaySvrID": relaySvrID, "gameseq": gameSeq})
                    print('对局数', len(data_list))
            if continue_win_event4:
                key_point_battle_list = continue_win_event4.get("key_point_battle_list")
                print("key_point_battle_list", key_point_battle_list)
                if key_point_battle_list:
                    for i in key_point_battle_list:
                        battle_video_url = i.get('battle_video_url')
                        game_seq_re = re.search('game_seq=(.*?)&', battle_video_url)
                        relaySvrID_re = re.search('relay_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID_re = re.search('game_svr_entity=(.*?)&', battle_video_url)
                        gameSvrID = gameSvrID_re.group(1)
                        relaySvrID = relaySvrID_re.group(1)
                        gameSeq = game_seq_re.group(1)
                        data_list.append({"gameSvrID": gameSvrID, "relaySvrID": relaySvrID, "gameseq": gameSeq})
                    print('对局数', len(data_list))

            if not data_list:
                print("no_result")
                pass
            return data_list
    return None


def get_user_data(gameSvrId, relaySvrID, gameSeq, open_id, roleId='', paixu=1):
    pass


if __name__ == '__main__':
    #     token = ''
    #     serverId = ''
    #     toOpenid = ''
    #     resp_json = get_shengcheng(token, serverId, toOpenid)
    # print(resp_json)

    # openid = 'owanlsnSqiwNnd72Y3KpZpxxcb4c',
    openid = 'owanlskn3-DCpZnhRUWgApywOZd0',
    content_id = 'efkAJCm88tIf_KiRmh0U0g0ABW7nvOsKjDkz38PXpiY',
    event_type = 'promotioneventtype',
    Cookie = 'cookie_passkey=1; uin=MTQxMjYxODYzNA%3D%3D; pass_ticket=zOzwQwUkdsFwhn9vChIZhDetyxXA45TqwZS7%2BJ7yzphVXb7eoxr9wg1AaDJ%2BC3EU; key=5e6d38340dec3db44d1cf179f3d68e1f69a1c7fd9e73e4f45e810963813bd402f00fb787c94e3cd87b1cf0247941b5666dd26858ac182a3ecb2f16869e614b474d04e580071a0adba01e14f932a81e4da735484d6131e5c3ba3e1699482d85f70489a402b18a927b17b4d93d3a49b54285d4824d96bf611bfae9748193c9422d'
    # Cookie = ''
    j = get_open_id(openid, content_id, event_type, Cookie)
print(j)
