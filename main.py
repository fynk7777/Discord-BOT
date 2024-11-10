import os
import re
import discord
import random
import time
from flask import Flask
from keep_alive import keep_alive
from math import sqrt
import ctypes
import sys
from datetime import datetime, timedelta

msg = ""

# prime.txt から素数をロードする
def load_primes(filename="prime.txt"):
    with open(filename, "r") as file:
        primes = [int(line.strip()) for line in file if line.strip().isdigit()]
    return primes

# 新たに発見した素数を prime.txt に追加する
def save_prime(prime, filename="prime.txt"):
    with open(filename, "a") as file:
        file.write(f"{prime}\n")

def factorization(n):
    factors = []
    if n < 1:
        return [-1]
    elif not isinstance(n, int):
        return [-1]
    elif n == 1:
        return [1]

    # prime.txt から素数リストをロード
    primes = load_primes()
    n1 = n
    max_prime = max(primes)

    # prime.txt の素数を使って素因数分解
    for prime in primes:
        if prime > n1:
            break
        while n1 % prime == 0:
            n1 //= prime
            factors.append(prime)
            if n1 == 1:
                return factors

    # prime.txt にない範囲外の素数を計算してファイルに保存
    for i in range(max_prime + 1, int(sqrt(n1)) + 1):
        if all(i % p != 0 for p in primes):
            # 新しい素数を見つけた場合
            primes.append(i)
            save_prime(i)  # prime.txt に保存
        if n1 % i == 0:
            while n1 % i == 0:
                n1 //= i
                factors.append(i)
                if n1 == 1:
                    return factors

    # 残りの部分が素数の場合
    if n1 != 1:
        factors.append(n1)
        save_prime(n1)  # prime.txt に保存

    return factors

def factorize(num):
    start = time.time()
    result = factorization(num)
    end = time.time()
    time_diff = end-start
    global msg
    msg = f'{num}: {result}\n{time_diff}秒'
    print(f"{num}:{result}")
    print(f"{time_diff}秒")

def random_number_from_range(num1, num2=None):
    """指定された範囲からランダムな整数を生成する関数"""
    if num2 is None:
        # 1からnum1までの範囲でランダムな整数を生成
        num2 = num1
        num1 = 1

    return random.randint(int(num1), int(num2))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'BOTが起動しました。Logged in as {client.user}')

@client.event
async def on_message(message):
    message_content = message.content
    channel = message.channel
    user = message.author
    user_id = user.id
    if message.author == client.user:
        return

    if message_content == "b!bot test":
        await message.channel.send("githubにより起動しています")
    elif message_content == "b!bot stop":
        if user_id == "1212687868603007067":
            embed = discord.Embed(
                title="BOTを停止します",
                color="0xff0000",
                timestamp=datetime.utcnow()
            )
            await message.channel.send(embed=embed)

    # avg. コマンド処理
    avg_match = re.match(r'^avg\.\s*([\d\s]+)', message.content)
    if avg_match:
        numbers = list(map(int, avg_match.group(1).split()))
        average = sum(numbers) / len(numbers)
        response = f'average: {average:.2f}'  # 小数点以下2桁で表示
        await message.channel.send(response)
        return

    # total. コマンド処理
    total_match = re.match(r'^total\.\s*([\d\s]+)', message.content)
    if total_match:
        numbers = list(map(int, total_match.group(1).split()))
        response = f'total: {sum(numbers)}'
        await message.channel.send(response)
        return

    # calc. コマンド処理
    calc_match = re.match(r'^calc\.\s*(.+)', message.content)
    if calc_match:
        expression = calc_match.group(1)
        try:
            # `eval` を使って数式を計算
            result = eval(expression)
            response = f'calculation: {result}'
        except Exception as e:
            # エラーが発生した場合はエラーメッセージを表示
            response = f'calculation error: {str(e)}'
        await message.channel.send(response)
        return

    # prime. コマンド処理
    prime_match = re.match(r'^prime\.\s*(\d+)', message.content)
    if prime_match:
        number = int(prime_match.group(1))
        factorize(number)
        response = msg
        await message.channel.send(response)
        return

    # random. コマンド処理
    random_match = re.match(r'^random\.\s*([\d\.]+)(?:\s+([\d\.]+))?', message.content)
    if random_match:
        num1 = float(random_match.group(1))
        num2 = float(random_match.group(2)) if random_match.group(2) else None
        random_number = random_number_from_range(num1, num2)
        response = f'random number: {random_number}'
        await message.channel.send(response)
        return

TOKEN = os.getenv("DISCORD_TOKEN")

# Flaskサーバーを起動して、ボットを維持する
keep_alive()

# ボットを実行
client.run(TOKEN)

