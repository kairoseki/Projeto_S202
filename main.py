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

# menu.py
import requests

# Definir a URL base da API
BASE_URL = 'http://127.0.0.1:5000/produtos'

def listar_produtos():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        produtos = response.json()
        if produtos:
            print("\nLista de Produtos:")
            for produto in produtos:
                print(f"ID: {produto['_id']}, Nome: {produto['nome']}, Preço: {produto['preco']}, Quantidade: {produto['quantidade']}")
        else:
            print("\nNenhum produto encontrado!")
    else:
        print("Erro ao listar os produtos!")

def criar_produto():
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição do produto: ")
    preco = float(input("Digite o preço do produto: "))
    quantidade = int(input("Digite a quantidade em estoque: "))
    
    produto = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "quantidade": quantidade
    }
    
    response = requests.post(BASE_URL, json=produto)
    if response.status_code == 201:
        print(f"Produto '{nome}' criado com sucesso!")
    else:
        print("Erro ao criar produto!")

def atualizar_produto():
    listar_produtos()
    produto_id = input("\nDigite o ID do produto a ser atualizado: ")
    
    nome = input("Digite o novo nome do produto: ")
    descricao = input("Digite a nova descrição do produto: ")
    preco = float(input("Digite o novo preço do produto: "))
    quantidade = int(input("Digite a nova quantidade em estoque: "))
    
    produto_atualizado = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "quantidade": quantidade
    }
    
    response = requests.put(f"{BASE_URL}/{produto_id}", json=produto_atualizado)
    if response.status_code == 200:
        print(f"Produto '{produto_id}' atualizado com sucesso!")
    else:
        print("Erro ao atualizar o produto!")

def deletar_produto():
    listar_produtos()
    produto_id = input("\nDigite o ID do produto a ser deletado: ")
    
    response = requests.delete(f"{BASE_URL}/{produto_id}")
    if response.status_code == 200:
        print(f"Produto '{produto_id}' deletado com sucesso!")
    else:
        print("Erro ao deletar o produto!")

def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1. Listar produtos")
        print("2. Criar novo produto")
        print("3. Atualizar produto")
        print("4. Deletar produto")
        print("5. Sair")

        opcao = input("\nDigite a opção desejada (1-5): ")

        if opcao == '1':
            listar_produtos()
        elif opcao == '2':
            criar_produto()
        elif opcao == '3':
            atualizar_produto()
        elif opcao == '4':
            deletar_produto()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Rodar o menu
if __name__ == '__main__':
    menu()
