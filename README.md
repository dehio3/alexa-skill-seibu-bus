# alexa-skill-seibu-bus
### 概要
- 西武バスのロケーション検索結果URLを設定するとバスの到着予定時刻を読み上げます
- 経路のパターンは複数指定可能です

### 使い方
- [西武バスロケーションサイト](http://transfer.navitime.biz/seibubus-dia/pc/map/Top?window=busLocation)から乗りたい経路を検索します。
- 検索結果のURLをコピーします。
- [main.py](/main.py)のURLリストに、読み上げたいバス停名と、検索結果のURLを入力します。
```python
URL = {
    "交番前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110462&goalId=00110468",
    "都営住宅前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110450&goalId=00110468"
}
```
