import os
import tkinter as tk
from tkinter import messagebox

def validar_nome(nome):
    if not nome:
        raise ValueError("O nome não pode estar vazio.")
    if any(char.isdigit() for char in nome):
        raise ValueError("O nome não pode conter números.")
    return nome

def validar_matricula(matricula):
    if not matricula.isdigit():
        raise ValueError("A matrícula deve conter apenas números.")
    return matricula

def validar_telefone(telefone):
    if not telefone.isdigit() or len(telefone) < 9:
        raise ValueError("O telefone deve conter apenas números e ter pelo menos 9 dígitos.")
    return telefone

def escrever_arquivo(nome_arquivo, conteudo):
    with open(nome_arquivo, 'w') as f:
        f.write(conteudo)

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Arquivo não encontrado."
    except IOError:
        return "Erro ao ler o arquivo."

def excluir_arquivo(nome_arquivo):
    try:
        os.remove(nome_arquivo)
        messagebox.showinfo("Sucesso", "Arquivo excluído com sucesso.")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir o arquivo: {e}")

def cadastrar_aluno():
    nome = entry_nome.get()
    matricula = entry_matricula.get()
    telefone = entry_telefone.get()

    try:
        validar_nome(nome)
        validar_matricula(matricula)
        validar_telefone(telefone)

        conteudo = f"Nome: {nome}\nMatrícula: {matricula}\nTelefone: {telefone}"
        escrever_arquivo("aluno.txt", conteudo)
        messagebox.showinfo("Sucesso", "Dados gravados com sucesso.")
        limpar_campos()
    except ValueError as e:
        messagebox.showerror("Erro de validação", str(e))

def mostrar_dados():
    conteudo = ler_arquivo("aluno.txt")
    txt_dados.delete("1.0", tk.END)
    txt_dados.insert(tk.END, conteudo)

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_matricula.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)

root = tk.Tk()
root.title("Cadastro de Aluno")
root.geometry("400x450")

tk.Label(root, text="Nome:").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

tk.Label(root, text="Matrícula:").pack()
entry_matricula = tk.Entry(root)
entry_matricula.pack()

tk.Label(root, text="Telefone:").pack()
entry_telefone = tk.Entry(root)
entry_telefone.pack()

tk.Button(root, text="Cadastrar", command=cadastrar_aluno).pack(pady=5)
tk.Button(root, text="Ler Dados", command=mostrar_dados).pack(pady=5)
tk.Button(root, text="Alterar Dados", command=cadastrar_aluno).pack(pady=5)
tk.Button(root, text="Excluir Dados", command=lambda: excluir_arquivo("aluno.txt")).pack(pady=5)
tk.Button(root, text="Sair", command=root.quit).pack(pady=5)

tk.Label(root, text="Dados do Aluno:").pack()
txt_dados = tk.Text(root, height=10, width=40)
txt_dados.pack()

root.mainloop()
