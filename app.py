from flask import Flask, render_template
from gpiozero import LED
from random import choice

led = LED(17)  # GPIO pin for the LED

vis = 0
curiosidades = [
    "Gosto muito de programar em Python.",
    "Adoro jogar Andebol e jogo no SCP",
    "Tenho vários cubos mágicos",
    "Tenho 4 irmãos, 2 rapazes e 2 raparigas",
    "A minha cadela chama-se Zucca(abóbora em italiano, pois era laranja quando a adotámos) e é mais velha que eu, tem 17 anos",
]

app = Flask(__name__)


@app.route('/')
def index():
    curiosidade = choice(curiosidades)
    global vis
    vis += 1

    return render_template("index.html",
                           led_status=led.is_lit,
                           visitas=vis,
                           curiosidade=curiosidade)


@app.route('/led/<string:status>')
def led(status):
    if status == "ON":
        led.on()
        return "LED ligado"
    elif status == "OFF":
        led.off()
        return "LED desligado"
    else:
        return "ERROR", 404


app.run(host="0.0.0.0", port=8082,  debug=True) 