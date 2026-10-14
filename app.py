from flask import Flask
import random

app = Flask(__name__)

piadas = [
    "Por que o livro de matemática se suicidou? Porque tinha muitos problemas.",
    "Por que o computador foi ao médico? Porque estava com um vírus.",
    "Por que o tomate foi ao banco? Porque ele queria se tornar um extrato.",
    "Por que o peixe não gosta de jogar cartas? Porque ele tem medo de ser pescado.",
    "O que o zero disse para o oito? Belo cinto!",
    "Dois átomos estavam andando na rua. Um deles disse: 'Acho que perdi um elétron.' O outro perguntou: 'Você tem certeza?' E o primeiro respondeu: 'Sim, estou positivo!'",
    "Por que o coelho atravessou a estrada? Para ir ao bar do outro lado.",
    "Minha mãe me disse para não brincar com fogo, mas eu não a ouvi. Agora estou queimando de vergonha.",]

@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/piada')
def piada():
    return random.choice(piadas) 


@app.route('/piada/<int:id>', methods=['GET'])
def piada(id):
    if id < 1 or id > len(piadas):
        return "Piada não encontrada.", 404
    return piadas[id-1] 






app.run(host="0.0.0.0", port=8080) 