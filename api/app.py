from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Inicialização
app = Flask(__name__)
CORS(app)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@banco:5432/biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Diretório para uploads
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Modelo Livro
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200), nullable=True)

# Cria as tabelas automaticamente
with app.app_context():
    db.create_all()

# Rota para listar livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    livros = Livro.query.all()
    resultado = []
    for livro in livros:
        resultado.append({
            'id': livro.id,
            'titulo': livro.titulo,
            'autor': livro.autor,
            'foto': f'/uploads/{livro.foto}' if livro.foto else None
        })
    return jsonify(resultado)

# Rota para adicionar livro
@app.route('/livros', methods=['POST'])
def adicionar_livro():
    titulo = request.form.get('titulo')
    autor = request.form.get('autor')
    foto = request.files.get('foto')

    filename = None
    if foto:
        filename = foto.filename
        caminho_foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(caminho_foto)

    novo_livro = Livro(titulo=titulo, autor=autor, foto=filename)
    db.session.add(novo_livro)
    db.session.commit()

    return jsonify({'mensagem': 'Livro adicionado com sucesso!'})

# Servir imagens do diretório /uploads
@app.route('/uploads/<filename>')
def get_imagem(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Início da aplicação
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
