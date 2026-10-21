from flask import Flask, jsonify, request
from flask_cors import CORS
import random


visitas = 0

app = Flask(__name__)
CORS(app)

piadas = [
    {
        "id": 1,
        "nome": "Por que o livro de matemática se suicidou? Porque tinha muitos problemas.",
        "origem": "engraçado"
    },
    {
        "id": 2,
        "nome": "Por que o computador foi ao médico? Porque estava com um vírus.",
        "origem": "médio"
    },
    {
        "id": 3,
        "nome  ": "Por que o tomate foi ao banco? Porque ele queria se tornar um extrato.",
        "origem": "engraçado"
    },
    {
        "id": 4,
        "nome": "Por que o peixe não gosta de jogar cartas? Porque ele tem medo de ser pescado.",
        "origem": "seca"
    },
    {
        "id": 5,
        "nome": "O que o zero disse para o oito? Belo cinto!",
        "origem": "seca"
    },
    {
        "id": 6,
        "nome": "Dois átomos estavam andando na rua. Um deles disse: 'Acho que perdi um elétron.' O outro perguntou: 'Você tem certeza?' E o primeiro respondeu: 'Sim, estou positivo!'",
        "origem": "engraçado"
    },
    {
        "id": 7,
        "nome": "Por que o coelho atravessou a estrada? Para ir ao bar do outro lado.",
        "origem": "pior piada de sempre"
    },
    {
        "id": 8,
        "nome": "Minha mãe me disse para não brincar com fogo, mas eu não a ouvi. Agora estou queimando de vergonha.",
        "origem": "seca"
    }]

@app.route('/')
def index():
    visitas += 1
    return jsonify({"visitas": visitas})


@app.route('/piada')
def piada():
    return jsonify(random.choice(piadas))


@app.route('/piada/<int:id>', methods=['GET'])
def get_piada(id):
    if id < 1 or id > len(piadas):
        return jsonify({"error": "Piada não encontrada."}), 404
    return jsonify(piadas[id-1]) 


@route('/')
def get_visitas():
    


app.run(host="0.0.0.0", port=8082) 