import os

def validar_nome(nome):
    if not nome:
        raise ValueError("O nome não pode estar vazio.")
    if any(char.isdigit() for char in nome):
        raise ValueError("O nome não pode conter números.")
    return nome

def validar_matricula(matricula):
    if not matricula.isdigit():
        raise ValueError("O número de matrícula deve conter apenas números.")
    return matricula

def validar_telefone(telefone):
    if not telefone.isdigit() or len(telefone) < 9:
        raise ValueError("O telefone deve conter apenas números e ter pelo menos 9 dígitos.")
    return telefone

def escrever_arquivo(nome_arquivo, conteudo):
    try:
        with open(nome_arquivo, 'w') as f:
            f.write(conteudo)
    except IOError:
        print("Erro: Não foi possível escrever no arquivo.")

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("Erro: O arquivo não existe.")
    except IOError:
        print("Erro ao tentar ler o arquivo.")

def fechar_arquivo(file):
    try:
        file.close()
    except AttributeError:
        print("Erro: Tentativa de fechar um arquivo que não foi aberto.")

def main():
    try:
        nome = input("Digite o nome do aluno: ")
        validar_nome(nome)
        
        matricula = input("Digite o número de matrícula: ")
        validar_matricula(matricula)
        
        telefone = input("Digite o telefone do aluno: ")
        validar_telefone(telefone)
        
        conteudo = f"Nome: {nome}\nMatrícula: {matricula}\nTelefone: {telefone}"
        escrever_arquivo("aluno.txt", conteudo)
        
        print("Dados gravados com sucesso!")
        print("Lendo arquivo salvo:")
        print(ler_arquivo("aluno.txt"))
        
    except ValueError as e:
        print(f"Erro de validação: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":  
    main()

