from flask import Flask, render_template
from random import choice

vis = 0
curiosidades = [
    "Gosto muito de programar em Python.",
    "Adoro jogar Andebol e jogo no SCP",
    "Tenho vários cubos mágicos",
    "Tenho 4 irmãos, 2 rapazes e 2 raparigas",
    "A minha cadela chama-se Zucca(de abóbora em italiano, pois era laranja quando a adotámos) e é mais velha que eu, tem 17 anos",
]

app = Flask(__name__)


@app.route('/')
def index():
    curiosidade = choice(curiosidades)
    global vis
    vis += 1
    return render_template('index.html', visitas=vis, curiosidade=curiosidade)

app.run(host="0.0.0.0", port=8082,  debug=True) 