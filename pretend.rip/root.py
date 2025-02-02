import discord
import threading
from tools.bot import Pretend
from tools.helpers import PretendContext
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bot = Pretend()

@app.route("/stats", methods=["GET"])
def stats():
    members = sum(guild.member_count for guild in bot.guilds)
    servers = len(bot.guilds)
    return jsonify({"members": members, "servers": servers})

def run_flask():
    print("Starting Flask server...")  # Debug print
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)