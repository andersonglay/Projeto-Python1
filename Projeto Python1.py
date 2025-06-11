import os
import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox, ttk

def inicializar_banco():
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

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

def inserir_aluno(nome, matricula, telefone):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO alunos (nome, matricula, telefone) VALUES (?, ?, ?)", (nome, matricula, telefone))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Matrícula já cadastrada.")
    finally:
        conn.close()

def buscar_aluno_por_matricula(matricula):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, matricula, telefone FROM alunos WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def excluir_aluno_por_matricula(matricula):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alunos WHERE matricula = ?", (matricula,))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows

def alterar_aluno(nome, matricula, telefone):
    conn = sqlite3.connect("alunos.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE alunos SET nome = ?, telefone = ? WHERE matricula = ?", (nome, telefone, matricula))
    conn.commit()
    rows = cursor.rowcount
    conn.close()
    return rows

def sair():
    root.destroy()
    sys.exit()

def cadastrar_aluno():
    nome = entry_nome.get()
    matricula = entry_matricula.get()
    telefone = entry_telefone.get()
    try:
        validar_nome(nome)
        validar_matricula(matricula)
        validar_telefone(telefone)
        inserir_aluno(nome, matricula, telefone)
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
        limpar_campos()
    except ValueError as e:
        messagebox.showerror("Erro de validação", str(e))

def atualizar_aluno():
    nome = entry_nome.get()
    matricula = entry_matricula.get()
    telefone = entry_telefone.get()
    try:
        validar_nome(nome)
        validar_matricula(matricula)
        validar_telefone(telefone)
        rows = alterar_aluno(nome, matricula, telefone)
        if rows:
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso.")
        else:
            messagebox.showerror("Erro", "Aluno não encontrado para atualizar.")
    except ValueError as e:
        messagebox.showerror("Erro de validação", str(e))

def buscar_aluno():
    matricula = entry_busca_matricula.get()
    if not matricula:
        messagebox.showerror("Erro", "Informe a matrícula para buscar.")
        return
    try:
        validar_matricula(matricula)
        resultado = buscar_aluno_por_matricula(matricula)
        txt_dados.delete("1.0", tk.END)
        if resultado:
            nome, matricula, telefone = resultado
            txt_dados.insert(tk.END, f"Nome: {nome}\nMatrícula: {matricula}\nTelefone: {telefone}")
        else:
            txt_dados.insert(tk.END, "Aluno não encontrado.")
    except ValueError as e:
        messagebox.showerror("Erro de validação", str(e))

def excluir_aluno():
    matricula = entry_busca_matricula.get()
    if not matricula:
        messagebox.showerror("Erro", "Informe a matrícula para excluir.")
        return
    try:
        validar_matricula(matricula)
        rows = excluir_aluno_por_matricula(matricula)
        if rows:
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso.")
            txt_dados.delete("1.0", tk.END)
        else:
            messagebox.showerror("Erro", "Aluno não encontrado.")
    except ValueError as e:
        messagebox.showerror("Erro de validação", str(e))

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_matricula.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_busca_matricula.delete(0, tk.END)
    txt_dados.delete("1.0", tk.END)
    
inicializar_banco()
root = tk.Tk()
root.title("Sistema de Cadastro de Alunos")
root.geometry("450x550")

estilo = ttk.Style()
estilo.theme_use("clam")

frame_cadastro = ttk.LabelFrame(root, text="Cadastro de Aluno")
frame_cadastro.pack(padx=10, pady=10, fill="x")

ttk.Label(frame_cadastro, text="Nome:").pack(anchor='w')
entry_nome = ttk.Entry(frame_cadastro)
entry_nome.pack(fill='x')

ttk.Label(frame_cadastro, text="Matrícula:").pack(anchor='w')
entry_matricula = ttk.Entry(frame_cadastro)
entry_matricula.pack(fill='x')

ttk.Label(frame_cadastro, text="Telefone:").pack(anchor='w')
entry_telefone = ttk.Entry(frame_cadastro)
entry_telefone.pack(fill='x')

botoes_cadastro = ttk.Frame(frame_cadastro)
botoes_cadastro.pack(pady=5)
ttk.Button(botoes_cadastro, text="Cadastrar", command=cadastrar_aluno).pack(side="left", padx=5)
ttk.Button(botoes_cadastro, text="Alterar", command=atualizar_aluno).pack(side="left", padx=5)

frame_busca = ttk.LabelFrame(root, text="Buscar / Excluir Aluno")
frame_busca.pack(padx=10, pady=10, fill="x")

ttk.Label(frame_busca, text="Matrícula:").pack(anchor='w')
entry_busca_matricula = ttk.Entry(frame_busca)
entry_busca_matricula.pack(fill='x')

btns = ttk.Frame(frame_busca)
btns.pack(pady=5)
ttk.Button(btns, text="Buscar", command=buscar_aluno).pack(side="left", padx=5)
ttk.Button(btns, text="Excluir", command=excluir_aluno).pack(side="left", padx=5)

ttk.Label(root, text="Resultado:").pack(padx=10, anchor='w')
txt_dados = tk.Text(root, height=8, width=50)
txt_dados.pack(padx=10, pady=5)

frame_footer = ttk.Frame(root)
frame_footer.pack(pady=10)
ttk.Button(frame_footer, text="Limpar Campos", command=limpar_campos).pack(side="left", padx=10)
ttk.Button(frame_footer, text="Sair", command=sair).pack(side="right", padx=10)

root.mainloop()
