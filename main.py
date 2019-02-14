#!/usr/bin/python3
# coding: UTF-8

import urllib.request
from bs4 import BeautifulSoup

"""
辞書型でURLリストを作成
    key: 最寄りのバス停名
    value: 検索結果URL
"""
URL = { \
"交番前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110462&goalId=00110468" , \
"都営住宅前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110450&goalId=00110468" \
}

def buss_time(url):
    """到着時刻取得関数
    
    Args:
        param1 (str):   西武バスバスロケーションページの検索結果URL
                        以下のサイトより時刻検索を行い、検索結果のURLを入力する
                        http://transfer.navitime.biz/seibubus-dia/pc/map/Top?window=busLocation
    
    Return:
        str: 到着予定時刻 (ex:約10分,約20分,約24)
    """

    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # div要素全てを摘出する
    div = soup.find_all("div")

    # 変数の初期化
    time_data = "" # 到着時刻
    time_list = [] # 到着時刻のリスト
    print_flg = 0
    
    # for分で全てのdiv要素の中からClass="plannedTime"となっている物を探します
    for tag in div:

        # plannedTime の次のdivタグの場合（出力フラグが設定されていた場合）
        if print_flg == 1:
            # タグの値を取得
            time_data = tag.string
            # 余分な空白を削除
            time_data = time_data.split()

            # 所要時間は出力しないように要素をチェック
            if len(time_data) == 2:
                # message = time_data[1]
                # 到着時刻をリストに追加
                time_list.append(time_data[1])
                #print(message)
            # 出力フラグをリセット
            print_flg = 0

        # 先頭の3台分の到着情報を取得
        if len(time_list) == 3:
            break

        # classの設定がされていない要素は、tag.get("class").pop(0)を行うことのできないでエラーとなるため、tryでエラーを回避する
        try:
            # tagの中からclass="n"のnの文字列を摘出します。複数classが設定されている場合があるので
            # get関数では配列で帰ってくる。そのため配列の関数pop(0)により、配列の一番最初を摘出する
            # <span class="hoge" class="foo">  →   ["hoge","foo"]  →   hoge
            string_ = tag.get("class").pop(0)

            # 摘出したclassの文字列にplannedTimeと設定されているかを調べます
            if string_ in "plannedTime":
                # plannedTimeの次のdivタグが時刻のため、フラグをセットする
                print_flg = 1
        except:
            # パス→何も処理を行わない
            pass

    # 到着時間のリストを文字列として連結
    message = ','.join(time_list)
    
    return message

def main(event, context):
    """ 指定したURLリストのから到着時刻を取得しAlexaへJSONデータを返す
    
    """
    
    #リストの作成
    time_messages = []
    
    for key, value in URL.items():
        #バス停毎の待ち時間を取得
        time = buss_time(value)
        
        #メッセージを作成
        # ex) 交番前は,約11分,約24分,約28分
        time_message = '{0}は,{1}'.format(key,time)
        #全てのバス停のメッセージを結合
        time_messages.append(time_message)
    
    # リスト型のメッセージを文字列に変更
    message = ','.join(time_messages)
    
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': message + 'で到着します',
            }
        }
    }
    
    return response


# テスト用
if __name__ == '__main__':
    print(main(None, None))
