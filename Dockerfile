# ベースイメージの指定
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# setup.pyとC拡張モジュールのソースコードをコピー
COPY setup.py .
COPY factorizer.c .

# C拡張モジュールのビルド
RUN python setup.py build_ext --inplace

# アプリケーションのソースコードをコピー
COPY . .

# サーバーを起動するスクリプトを実行
CMD ["python", "main.py"]
