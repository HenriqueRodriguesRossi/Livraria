from flask import Flask, jsonify, request
import sqlite3

'''banco = sqlite3.connect('livraria.db')
cursor = banco.cursor()
cursor.execute("CREATE TABLE livros(id INTEGER PRIMARY KEY AUTOINCREMENT, título TEXT, autor TEXT)")'''

app = Flask(__name__)

#Lista todos os livros
@app.route('/livros', methods=['GET'])
def retornaTodosOsLivros ():
	banco = sqlite3.connect('livraria.db')
	cursor = banco.cursor()
	cursor.execute("SELECT * FROM livros")
	consulta_no_banco = cursor.fetchall()
	banco.close()

	return jsonify(consulta_no_banco)

#Retorna livro por título
@app.route('/livros/<string:titulo>', methods=['GET'])
def retornaLivroPeloTitulo(titulo):
	banco = sqlite3.connect('livraria.db')
	cursor = banco.cursor()
	cursor.execute('SELECT * FROM livros WHERE título = ?', (titulo,))
	livro = cursor.fetchone()
	banco.close()

	if livro: 
		return jsonify(livro)
	else: 
		return jsonify({"Mensagem": "Livro nao encontrado!"})

#Retorna livro por id
@app.route('/livros/id', methods=['GET'])
def retornaLivroPeloId (id):
	banco = sqlite3.connect('livraria.db')
	cursor = banco.cursor()
	cursor.execute('SELECT * FROM livros WHERE id= ?', (id))
	retorna_id = cursor.fetchone()
	banco.close()

	if retorna_id: 
		return jsonify(retorna_id)
	else: 
		return jsonify({"Mensagem": "Livro nao encontrado!"})


#Altera livro 
@app.route('/livros/alterar/<string:titulo>', methods=['PUT'])
def alterandoLivro(titulo):
	banco = sqlite3.connect('livraria.db')
	cursor = banco.cursor()
	cursor.execute('SELECT * FROM livros WHERE título = ?', (titulo,))
	livro = cursor.fetchone()

	if livro:
		novo_titulo = request.json.get('título')
		novo_autor = request.json.get('autor')
		
		if novo_titulo is None or novo_autor is None:
			return jsonify({"Mensagem": "Autor ou título inválidos, tente novamente!"})
		else: 
			cursor.execute('UPDATE livros SET título = ?, autor = ? WHERE título = ?', (novo_titulo, novo_autor, titulo))
			banco.commit()
			banco.close()

			return jsonify({"Mensagem": "Livro alterado com sucesso!"})
	else:
		banco.close()

		return jsonify({"Mensagem": "Livro nao encontrado!"})

#Cadastra novos livros 
@app.route('/livros/cadastrar', methods=['POST'])
def cadastrandoNovosLivros ():
	titulo = request.json.get('título')
	autor = request.json.get('autor')

	banco = sqlite3.connect('livraria.db')
	cursor = banco.cursor()
	cursor.execute("SELECT * FROM livros WHERE título = ? AND autor = ?", (titulo, autor))
	livro = cursor.fetchone()

	if livro: 
		banco.close()
		return jsonify({"mensagem": "Livro já cadastrado!"})
	else: 
		if titulo is None or autor is None: 
			return jsonify({"Mensagem": "Título ou autor inválidos, tente novamente!"})
		else: 
			cursor.execute("INSERT INTO livros (título, autor) VALUES(?, ?)", (titulo, autor))
			banco.commit()
			banco.close()
			return jsonify({"Mensagem": "Livro cadastrado com sucesso!"})

#Deleta livros
@app.route('/livros/excluir', methods=['DELETE'])
def deletaLivros():
	deleta_livro = request.json.get('título')

	banco = sqlite3.connect('livraria.db')
	cursor = banco.cursor()
	cursor.execute('SELECT * FROM livros WHERE título = ?', (deleta_livro,))
	livro = cursor.fetchone()

	if livro:
		cursor.execute('DELETE FROM livros WHERE título= ?', (deleta_livro,))
		banco.commit()
		banco.close()

		return jsonify({"Mensagem": "Livro excluido com sucesso!"})
	else:
		banco.close()

		return jsonify({"Mensagem": "Livro nao encontrado!"})

#Fornecendo porta para rodar a api
app.run(port= 8080, host='localhost', debug= True)
