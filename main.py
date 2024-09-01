import os
import re
import discord
import random
from flask import Flask
from keep_alive import keep_alive
from math import sqrt

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def prime_factors(n):
    """与えられた整数の素因数分解を行う関数"""
    i = 2
    factors = []
    while i <= sqrt(n):
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def random_number_from_range(num1, num2=None):
    """指定された範囲からランダムな数値を生成する関数"""
    if num2 is None:
        # 1からnum1までの範囲でランダムな数値を生成
        num2 = num1
        num1 = 1

    # 数値に小数点が含まれているかを確認
    num1_is_integer = num1.is_integer()
    num2_is_integer = num2.is_integer()

    if num1_is_integer and num2_is_integer:
        # 両方が整数である場合、整数を返す
        return random.randint(int(num1), int(num2))
    else:
        # どちらかが少数である場合、少数を返す
        return round(random.uniform(num1, num2), max(len(str(num1).split('.')[1]), len(str(num2).split('.')[1])))

@client.event
async def on_ready():
    print(f'BOTが起動しました。Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    avg_match = re.match(r'^avg\.\s*([\d\s]+)', message.content)
    total_match = re.match(r'^total\.\s*([\d\s]+)', message.content)
    calc_match = re.match(r'^calc\.\s*(.+)', message.content)
    prime_match = re.match(r'^prime\.\s*(\d+)', message.content)
    random_match = re.match(r'^random\.\s*([\d\.]+)(?:\s+([\d\.]+))?', message.content)

    if avg_match:
        numbers = list(map(int, avg_match.group(1).split()))
        average = sum(numbers) / len(numbers)
        response = f'average: {average:.2f}'  # 小数点以下2桁で表示
        await message.channel.send(response)

    if total_match:
        numbers = list(map(int, total_match.group(1).split()))
        response = f'total: {sum(numbers)}'
        await message.channel.send(response)

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

    if prime_match:
        number = int(prime_match.group(1))
        factors = prime_factors(number)
        response = f'prime factors of {number}: ' + ' × '.join(map(str, factors))
        await message.channel.send(response)

    if random_match:
        num1 = float(random_match.group(1))
        num2 = float(random_match.group(2)) if random_match.group(2) else None
        random_number = random_number_from_range(num1, num2)
        response = f'random number: {random_number}'
        await message.channel.send(response)

TOKEN = os.getenv("DISCORD_TOKEN")

# Flaskサーバーを起動して、ボットを維持する
keep_alive()

# ボットを実行
client.run(TOKEN)
