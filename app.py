from flask import Flask, render_template, jsonify
from automacao import emitir_relatorio
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/emitir-relatorio', methods=['POST'])
def emitir():

    # roda em thread separada
    thread = threading.Thread(target=emitir_relatorio)
    thread.start()

    return jsonify({
        "mensagem": "Automação iniciada"
    })


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )