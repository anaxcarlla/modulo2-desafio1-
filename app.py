from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    # sqlite3 cria o arquivo database.db (nosso banco de dados foi criado) e se conect a variável com (conecta o banco de dados ao python)
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS(
                     id INTEGER PRIMARY KEY AUTOINCREMENT
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     image_url TEXT NOT NULL
                     )
""")
# (create table if not exists livros)__  criar tabela livros caso ela não existir, caso não tenha esse comando sempre que rodar o codigo ele vai recriar a tabela e dar erro

init_db()

@app.route("/doar", methods =["POST"])
# post para o usuário enviar as informações
def doar():
    dados = request.get_json()
    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("imagem_url")
    # o get pega a resposta do usuário em formato json

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro":"todas os campos são obrigatórios."}),400

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo,categoria,autor,image_url)
        VALUES ("{titulo}","{categoria}","{autor}","{image_url}")
""")
        conn.commit()
        return jsonify({"mensagem":"livro cadastrado com sucesso."}), 201

@app.route("/livros", methods=["GET"])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
       livros = conn.execute("SELECT * FROM LIVROS").fetchall()
       
       for item in livros:
           dicionario_livros = {
             "id":item[0]
             "titulo":item[1]
             "categoria":item[2]
             "autor":item[3]
             "imagem_url":item[4]
        }


#verifica se o script está sendo execultado
if __name__ == "__main__":
    app.run(debug=True)