import os
import yfinance as yf
import pytz
from datetime import datetime, timedelta

env = os.getenv("ENV")

def get_stock_price(event, context):
    print("get_stock_price 環境: ", env)
    ticker = None
    period = None
    interval = None

    # period: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
    # interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1d, 5d, 1wk, 1mo, 3mo

    if env == "local":
        ticker = "4755.T" # 楽天グループ
        # ticker = "2743.T" # ピクセルカンパニーズ
        period = "5d"
        interval = "60m"
    else:
        ticker = event.get("queryStringParameters", {}).get("ticker")
        period = event.get("queryStringParameters", {}).get("period")
        interval = event.get("queryStringParameters", {}).get("interval")

    # 東京のタイムゾーンを指定
    tokyo_tz = pytz.timezone('Asia/Tokyo')

    # 開始日と終了日を設定（例として前日と当日を指定）
    # start_date = (datetime.now(tokyo_tz) - timedelta(days=1)).strftime('%Y-%m-%d')
    # end_date = datetime.now(tokyo_tz).strftime('%Y-%m-%d')

    # 株価データの取得
    today_data = yf.download(tickers=ticker, period=period, interval=interval)

    # インデックスがすでにタイムゾーン付きの場合、tz_localize は不要
    if today_data.index.tz is None:
        # tz-naive の場合、UTC から東京のタイムゾーンに変換
        today_data.index = today_data.index.tz_localize('UTC').tz_convert(tokyo_tz)
    else:
        # tz-aware の場合、そのまま東京のタイムゾーンに変換
        today_data.index = today_data.index.tz_convert(tokyo_tz)
    # # インデックスを東京のタイムゾーンに変換
    # today_data.index = today_data.index.tz_convert(tokyo_tz)

    # インデックスをカラムに変換し、JST のタイムゾーンを保持
    today_data = today_data.reset_index()

    # # JSONファイルに書き出す
    # if env == "local":
    #     raw_json_data = today_data.to_json(orient="records", date_format="iso")
    #     with open("today_raw_data.json", "w") as file:
    #         file.write(raw_json_data)


    # 列名をシンプルに変換
    # today_data.columns = ['datetime', 'open', 'high', 'low', 'close', 'adjClose', 'volume']
    # 正しい順番に変更
    today_data.columns = ['datetime', 'adjClose', 'close', 'high', 'low', 'open', 'volume']
    # today_data.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'AjClose', 'Volume']

    # Datetime カラムを文字列として JST 形式でフォーマット
    today_data['datetime'] = today_data['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')

    # データを JSON 形式に変換
    # json_data = today_data.reset_index().to_json(orient="records", date_format="iso")
    json_data = today_data.to_json(orient="records", date_format="iso")

    # # JSONファイルに書き出す
    # if env == "local":
    #     with open("today_data.json", "w") as file:
    #         file.write(json_data)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json_data
    }

if env == "local":
    get_stock_price("event", "context")