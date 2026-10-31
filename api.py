from flask import Flask, current_app
from controler import LCUcontroler

app = Flask(__name__)

def lcu() -> LCUcontroler:
    return current_app.config["LCU"]

@app.route("/aceptarPartida", methods=["POST"])
def root():
    return lcu().acceptMatch()

