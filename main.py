# api.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

# Configurar a aplicação Flask
app = Flask(__name__)

# Configurar o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.supermercado
produtos_collection = db.produtos

# Endpoint para criar um novo produto
@app.route('/produtos', methods=['POST'])
def criar_produto():
    try:
        # Pega os dados enviados na requisição
        data = request.get_json()
        nome = data.get('nome')
        descricao = data.get('descricao')
        preco = data.get('preco')
        quantidade = data.get('quantidade')
        
        # Cria um novo produto
        novo_produto = {
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'quantidade': quantidade
        }
        
        # Insere o produto no banco de dados
        produto = produtos_collection.insert_one(novo_produto)
        
        return jsonify({'message': 'Produto criado com sucesso!', 'id': str(produto.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para obter todos os produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = list(produtos_collection.find())
    for produto in produtos:
        produto['_id'] = str(produto['_id'])  # Convertendo ObjectId para string
    return jsonify(produtos), 200

# Endpoint para obter um produto específico
@app.route('/produtos/<id>', methods=['GET'])
def obter_produto(id):
    produto = produtos_collection.find_one({'_id': ObjectId(id)})
    
    if produto:
        produto['_id'] = str(produto['_id'])
        return jsonify(produto), 200
    else:
        return jsonify({'error': 'Produto não encontrado!'}), 404

# Endpoint para atualizar um produto
@app.route('/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):
    try:
        data = request.get_json()
        
        updated_product = {
            'nome': data.get('nome'),
            'descricao': data.get('descricao'),
            'preco': data.get('preco'),
            'quantidade': data.get('quantidade')
        }
        
        result = produtos_collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': updated_product}
        )
        
        if result.matched_count > 0:
            return jsonify({'message': 'Produto atualizado com sucesso!'}), 200
        else:
            return jsonify({'error': 'Produto não encontrado!'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint para deletar um produto
@app.route('/produtos/<id>', methods=['DELETE'])
def deletar_produto(id):
    result = produtos_collection.delete_one({'_id': ObjectId(id)})
    
    if result.deleted_count > 0:
        return jsonify({'message': 'Produto deletado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Produto não encontrado!'}), 404

# Rodar a aplicação
if __name__ == '__main__':
    app.run(debug=True)
