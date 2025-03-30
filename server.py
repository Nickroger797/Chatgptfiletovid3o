from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

def run_server():
    app.run(host="0.0.0.0", port=8080)

def start_flask():
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
