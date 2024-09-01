import os
import re
import discord
import random
from flask import Flask
from keep_alive import keep_alive
from math import sqrt

# 素数のファイル名
PRIME_FILE = "Prime_number.txt"

def load_primes():
    """素数ファイルを読み込み、リストを返す"""
    if not os.path.exists(PRIME_FILE):
        # ファイルが存在しない場合は空のリストを返す
        return []
    with open(PRIME_FILE, "r") as f:
        primes = list(map(int, f.read().split()))
    return primes

def save_prime(prime):
    """新しい素数をファイルに保存する"""
    with open(PRIME_FILE, "a") as f:
        f.write(f"{prime}\n")

def is_prime(n):
    """素数かどうかをチェックする関数"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_factors(n):
    """与えられた整数の素因数分解を行う最適化された関数"""
    factors = []
    primes = load_primes()

    # 素数表から素因数分解
    for prime in primes:
        while n % prime == 0:
            factors.append(prime)
            n //= prime
        if n == 1:
            return factors

    # 素数表にない部分を標準の方法で素因数分解
    i = primes[-1] + 2 if primes else 3
    max_factor = int(sqrt(n)) + 1
    while i <= max_factor:
        if is_prime(i):
            while n % i == 0:
                factors.append(i)
                n //= i
            if is_prime(i) and i not in primes:
                save_prime(i)
        i += 2
        max_factor = int(sqrt(n)) + 1  # nが小さくなるので最大値も更新

    if n > 1:
        factors.append(n)
        if is_prime(n):
            save_prime(n)

    return factors

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
    if message.author == client.user:
        return

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
        factors = prime_factors(number)
        response = f'prime factors: ' + ' × '.join(map(str, factors))
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
