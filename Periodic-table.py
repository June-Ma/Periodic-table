import webbrowser
import threading
from flask import Flask, render_template, jsonify
from elements_data import ELEMENTS

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/elements")
def get_elements():
    return jsonify(ELEMENTS)

def _open(url):
    try:
        webbrowser.open(url, new=2)
    except Exception:
        pass

if __name__ == "__main__":
    port = 5000
    # If 5000 is busy, change port=5001 below.
    threading.Timer(0.8, _open, args=(f"http://127.0.0.1:{port}",)).start()
    app.run(debug=True, port=port)
