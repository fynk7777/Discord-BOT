# Pythonの公式イメージをベースにする
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY keep_alive.py keep_alive.py

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# コンテナが起動する際に実行されるコマンド
CMD ["python", "keep_alive.py"]
