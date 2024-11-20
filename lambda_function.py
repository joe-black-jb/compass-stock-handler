import json
import sys
import yfinance as yf
import os
from utils import get_stock_price

# リクエストのパスに応じて実行する関数を変更する
def route_request(event, context):
    print("ルーター起動⭐️")
    # print("event: ", event)
    # print("context: ", context)
    # リクエストパスの取得
    path = event['requestContext']['http']['path']

    # パスに応じて処理を分岐
    if path == "/stock":
        return get_stock_price(event, context)
    # elif path == "/other-endpoint":
    #     return other_endpoint(event, context)
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not Found'})
        }

def handler(event, context):
    print("環境: ", os.getenv("ENV"))
    # return 'Hello from AWS Lambda using Python' + sys.version + '!'
    return route_request(event, context)
