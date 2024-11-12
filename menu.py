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
