# ベースイメージ
FROM python:3.10-slim

# 必要なビルドツールをインストール
RUN apt-get update && apt-get install -y build-essential python3-dev

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt ./
COPY setup.py ./
COPY factorizer.c ./
COPY main.py ./
COPY keep_alive.py ./

# パッケージのインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# C拡張モジュールのビルドとインストール
RUN python setup.py build
RUN python setup.py install

# Flaskサーバーを起動して、ボットを維持するための設定
CMD ["python", "main.py"]
