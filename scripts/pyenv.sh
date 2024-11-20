# script.sh
#!/bin/bash

# 中断シグナル（SIGINT）をキャッチしてクリーンアップ処理を実行
cleanup() {
    echo "\033[31mスクリプトが中断されました。後続の処理は実行されません。\033[0m"  # 赤色
    exit 1
}

# SIGINT (Ctrl+C) をキャッチするように trap を設定
trap cleanup SIGINT

# .env ファイルを読み込む
if [ -f .env ]; then
    echo "\033[32m.env ファイルが見つかりました\033[0m"  # 緑色
    source .env
else
    echo "\033[31m.env ファイルが見つかりません\033[0m"  # 赤色
    exit 1
fi

python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
