import os
import re
import discord
from flask import Flask
from keep_alive import keep_alive

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

    avg_match = re.match(r'^avg\.\s*([\d\s]+)', message.content)
    total_match = re.match(r'^total\.\s*([\d\s]+)', message.content)

    if avg_match:
        numbers = list(map(int, avg_match.group(1).split()))
        average = sum(numbers) / len(numbers)
        response = f'average : {average}'  # 小数点以下2桁で表示
        await message.channel.send(response)

    if total_match:
        numbers = list(map(int, total_match.group(1).split()))
        response = f'total : {sum(numbers)}'
        await message.channel.send(response)

TOKEN = os.getenv("DISCORD_TOKEN")

# Flaskサーバーを起動して、ボットを維持する
keep_alive()

# ボットを実行
client.run(TOKEN)
