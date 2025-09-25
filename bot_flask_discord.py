import os
import discord
from discord.ext import commands
from flask import Flask, request
import threading

TOKEN = os.getenv("DISCORD_TOKEN")  # pega do Render

# Configurar intents
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask
app = Flask(__name__)

@app.route("/senddm", methods=["POST"])
def send_dm():
    data = request.json
    user_id = data.get("user_id")
    mensagem = data.get("mensagem")

    async def send():
        try:
            user = await bot.fetch_user(int(user_id))
            await user.send(mensagem)
            print(f"✅ Mensagem enviada para {user.name}")
        except Exception as e:
            print(f"❌ Erro: {e}")

    bot.loop.create_task(send())
    return {"status": "ok"}

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Rodar Flask em paralelo
threading.Thread(target=run_flask).start()

bot.run(TOKEN)
