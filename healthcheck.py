from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200  # Koyeb को बताएगा कि सर्वर सही से चल रहा है

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
