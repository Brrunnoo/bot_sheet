import os
import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import threading

# Pegando o token do bot de uma variável de ambiente
TOKEN = os.getenv("DISCORD_TOKEN")

# Configura intents para permitir DMs
intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True

# Inicializa o bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Flask app
app = Flask(__name__)

@app.route("/enviarDM", methods=["POST"])
def enviar_dm():
    try:
        data = request.json
        user_id = int(data["userId"])
        mensagem = data["mensagem"]

        # Envia mensagem de forma assíncrona
        async def _send():
            user = await bot.fetch_user(user_id)
            await user.send(mensagem)

        bot.loop.create_task(_send())

        return jsonify({"status": "ok", "detalhe": "Mensagem enviada!"})
    except Exception as e:
        return jsonify({"status": "erro", "detalhe": str(e)}), 500

# Roda o Flask em thread separada
def run_flask():
    app.run(host="0.0.0.0", port=3000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)