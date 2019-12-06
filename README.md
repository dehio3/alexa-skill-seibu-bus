# alexa-skill-seibu-bus
## 概要
- 西武バスのロケーション検索結果URLを設定するとバスの到着予定時刻を読み上げます
- 経路のパターンは複数指定可能です

## 使い方
- [西武バスロケーションサイト](http://transfer.navitime.biz/seibubus-dia/pc/map/Top?window=busLocation)から乗りたい経路を検索します。
- 検索結果のURLをコピーします。
- [main.py](/main.py)のURLリストに、読み上げたいバス停名と、検索結果のURLを入力します。
```python
URL = {
    "交番前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110462&goalId=00110468",
    "都営住宅前": "http://transfer.navitime.biz/seibubus-dia/pc/location/BusLocationResult?startId=00110450&goalId=00110468"
}
```

## Lambdaリリース方法
[serverless](https://serverless.com/)にてデプロイを自動化している為、serverlessコマンドの実行環境を事前に作成する必要があります。

### serverless install
[公式に手順](https://github.com/serverless/serverless#quick-start)に従いserverlessをインストールします。

### plugin install
個別のプラグインをインストールします。
```bash
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-plugin-aws-alerts
sls plugin install -n serverless-pseudo-parameters
```

### Deploy
ステージをパラメータにて指定し、デプロイします。
```
sls deploy --verbose --stage dev --alexaskill <alexaSkill Id>
```
