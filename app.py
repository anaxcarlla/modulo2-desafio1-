from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

@app.route("/doar", methods=["POST"])
def doar():

    dados = request.get_json()
    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")  # Corrigido: mantendo a coerência no nome

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    with sqlite3.connect("database.db") as conn:

        conn.execute(f"""
            INSERT INTO LIVROS (titulo, categoria, autor, image_url) 
            VALUES ("{titulo}","{categoria}", "{autor}", "{image_url}")
        """)
        conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201

@app.route("/livros", methods=["GET"])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

        livros_formatados = []
        for item in livros:
            dicionario_livros = {
                "id": item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor": item[3],
                "image_url": item[4]  # Nome corrigido para manter a coerência
            }
            livros_formatados.append(dicionario_livros)

    return jsonify(livros_formatados), 200  # Retorna JSON com status HTTP 200

if __name__ == "__main__":
    app.run(debug=True)
