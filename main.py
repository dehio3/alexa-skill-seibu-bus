#!/usr/bin/python3
# coding: UTF-8

import urllib.request
from bs4 import BeautifulSoup

"""
辞書型でURLリストを作成
    key: 最寄りのバス停名
    value: 検索結果URL
"""
URL = {
    "交番前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110462&goalId=00110468",
    "都営住宅前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110450&goalId=00110468"
}


def buss_time(url):
    """到着時刻取得関数

    Args:
        param1 (str):   西武バスバスロケーションページの検索結果URL
                        以下のサイトより時刻検索を行い、検索結果のURLを入力する
                        http://transfer.navitime.biz/seibubus-dia/pc/map/Top?window=busLocation

    Return:
        list: 到着予定時刻 (ex:['約2分', '約16分', '約30分'])
    """

    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # div要素全てを摘出する
    div = soup.find_all("div")

    # 変数の初期化
    time_data = ""  # 到着時刻
    time_list = []  # 到着時刻のリスト
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

    return time_list


def main(event, context):
    # リストの作成
    arrival_time = {}
    output_speech = []

    for key, value in URL.items():
        # バス停毎の待ち時間を取得
        time_list = buss_time(value)

        # 画面表示用辞書型を作成
        # {'交番前': ['約14分', '約26分', '約31分']}
        arrival_time[key] = time_list

        # 読み上げメッセージを作成
        # ex) 交番前は,約11分,約24分,約28分
        msg = ','.join(time_list)
        msg = '{0}は,{1}'.format(key, msg)
        # 全てのバス停のメッセージを結合
        output_speech.append(msg)

    # リスト型のメッセージを文字列に変更
    message = ','.join(output_speech)

    # ディスプレイメッセージを作成
    # https://developer.amazon.com/ja/docs/custom-skills/display-interface-reference.html#supported-markup
    display_text_content = ""
    for key, value in arrival_time.items():
        markup_message = '<font size="7">{}</font><br/><font size="5">{}</font><br/><br/>'.format(
            key, ','.join(value))
        display_text_content += markup_message

    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': message + 'で到着します',
            },
            "directives": [
                {
                    "type": "Display.RenderTemplate",
                    "template": {
                        "type": "BodyTemplate1",
                        "token": "TimeTable1",
                        "backButton": "VISIBLE",
                        "title": "バスの接近情報",
                        "textContent": {
                            "primaryText": {
                                "text": display_text_content,
                                "type": "RichText"
                            }
                        }
                    }
                }
            ],
            "shouldEndSession": "true"
        }
    }

    return response


if __name__ == '__main__':
    print(main(None, None))
