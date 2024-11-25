import os
import yfinance as yf
import pytz
from datetime import datetime, timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta

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
        period = "1d"
        interval = "5m"
    else:
        ticker = event.get("queryStringParameters", {}).get("ticker")
        period = event.get("queryStringParameters", {}).get("period")
        interval = event.get("queryStringParameters", {}).get("interval")

    # 東京のタイムゾーンを指定
    tokyo_tz = pytz.timezone('Asia/Tokyo')

    # 開始日と終了日を設定（例として前日と当日を指定）
    # パラメータに応じた期間設定
    # TODO: Lambda で動かすとエラーしていると思われる
    now = datetime.now(tokyo_tz)
    end_date = now.strftime('%Y-%m-%d')
    if period == "10y":
        start_date = (now - relativedelta(years=10)).strftime('%Y-%m-%d')

    # # 現在の日時
    # today = datetime.today()
    # # 1か月前の日時
    # one_month_ago = today - timedelta(days=30)

    # # 日付を文字列に変換 (yfinanceの形式に合わせる)
    # start_date = one_month_ago.strftime('%Y-%m-%d')
    # end_date = today.strftime('%Y-%m-%d')

    # 株価データの取得
    if period == "1d":
        stock_data = yf.download(tickers=ticker, period=period, interval=interval)
    elif period == "10y":
        stock_data = yf.download(tickers=ticker, start=start_date, end=end_date, interval=interval)
    # stock_data = yf.download(tickers=ticker, start=start_date, end=end_date, interval=interval)

    # インデックスがすでにタイムゾーン付きの場合、tz_localize は不要
    if stock_data.index.tz is None:
        # tz-naive の場合、UTC から東京のタイムゾーンに変換
        stock_data.index = stock_data.index.tz_localize('UTC').tz_convert(tokyo_tz)
    else:
        # tz-aware の場合、そのまま東京のタイムゾーンに変換
        stock_data.index = stock_data.index.tz_convert(tokyo_tz)

    # # インデックスを東京のタイムゾーンに変換
    # stock_data.index = stock_data.index.tz_convert(tokyo_tz)

    # インデックスをカラムに変換し、JST のタイムゾーンを保持
    stock_data = stock_data.reset_index()

    # # JSONファイルに書き出す
    # if env == "local":
    #     raw_json_data = stock_data.to_json(orient="records", date_format="iso")
    #     with open("today_raw_data.json", "w") as file:
    #         file.write(raw_json_data)

    # 移動平均の計算（例: 25日移動平均と75日移動平均）
    if period == "1d":
        stock_data['MA_25'] = None
        stock_data['MA_75'] = None
    else:
        stock_data['MA_25'] = stock_data['Close'].rolling(window=25).mean()  # 25日移動平均
        stock_data['MA_75'] = stock_data['Close'].rolling(window=75).mean()  # 75日移動平均
    # NaN を削除または埋める処理を追加
    # stock_data = stock_data.dropna(subset=['MA_25', 'MA_75'])  # NaN を削除
    # stock_data['MA_25'] = stock_data['MA_25'].fillna(0)
    # stock_data['MA_75'] = stock_data['MA_75'].fillna(0)
    # データの表示
    if env == "local":
        print("stock_data.tail()", stock_data.tail())  # 最後の数行を表示

    # 列名をシンプルに変換
    # stock_data.columns = ['datetime', 'open', 'high', 'low', 'close', 'adjClose', 'volume']
    # 正しい順番に変更
    stock_data.columns = ['datetime', 'adjClose', 'close', 'high', 'low', 'open', 'volume', 'ma25', 'ma75']
    # stock_data.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'AjClose', 'Volume']

    # Datetime カラムを文字列として JST 形式でフォーマット
    stock_data['datetime'] = stock_data['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')

    # データを JSON 形式に変換
    # json_data = stock_data.reset_index().to_json(orient="records", date_format="iso")
    json_data = stock_data.to_json(orient="records", date_format="iso")

    # JSONファイルに書き出す
    if env == "local":
        with open("stock_data.json", "w") as file:
            file.write(json_data)

    print("処理完了⭐️")
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json_data
    }

if env == "local":
    get_stock_price("event", "context")