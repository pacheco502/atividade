import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from tabulate import tabulate


# Classe Tarefa
class Tarefa:
    
    # Construtor
    def __init__(self):
        self.id_tarefa = None
        self.titulo = None
        self.descricao = None
        self.categoria = None
        self.status = None
        self.data_prazo = None
        self.nota = None

    # Métodos Getters e Setters
    def get_id_tarefa(self):
        return self.id_tarefa

    def set_id_tarefa(self, value):
        self.id_tarefa = value

    def get_titulo(self):
        return self.titulo

    def set_titulo(self, value):
        self.titulo = value

    def get_descricao(self):
        return self.descricao

    def set_descricao(self, value):
        self.descricao = value

    def get_categoria(self):
        return self.categoria

    def set_categoria(self, value):
        self.categoria = value

    def get_status(self):
        return self.status

    def set_status(self, value):
        self.status = value

    def get_data_prazo(self):
        return self.data_prazo

    def set_data_prazo(self, value):
        self.data_prazo = value

    def get_nota(self):
        return self.nota

    def set_nota(self, value):
        self.nota = value

    # Método de conexão ao banco de dados
    def conectar(self):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="gerenciador_tarefas"
            )
            if conexao.is_connected():
                return conexao
        except Error as e:
            print(f"Erro ao conectar: {e}")
            return None

    # Método inserir tarefa
    def inserir(self, titulo, descricao, categoria, status, data_prazo, nota):
        try:
            self.set_titulo(titulo)
            self.set_descricao(descricao)
            self.set_categoria(categoria)
            self.set_status(status)
            self.set_data_prazo(data_prazo)
            self.set_nota(nota)

            sql = '''
            INSERT INTO tb_tarefa (titulo, descricao, categoria, status, data_prazo, nota)
            VALUES (%s, %s, %s, %s, %s, %s)
            '''
            valores = (self.get_titulo(), self.get_descricao(), self.get_categoria(), self.get_status(), self.get_data_prazo(), self.get_nota())

            conectar = self.conectar()
            if conectar is None:
                return False
            else:
                dados = conectar.cursor()
                dados.execute(sql, valores)
                conectar.commit()
                return True
        except Error as e:
            print(f"Erro ao inserir tarefa: {e}")
            return False

    # Método alterar tarefa
    def alterar(self, id_tarefa, titulo=None, descricao=None, categoria=None, status=None, data_prazo=None, nota=None):
        try:
            self.set_id_tarefa(id_tarefa)

            campos = []
            valores = []

            if titulo is not None:
                campos.append("titulo = %s")
                valores.append(titulo)
            if descricao is not None:
                campos.append("descricao = %s")
                valores.append(descricao)
            if categoria is not None:
                campos.append("categoria = %s")
                valores.append(categoria)
            if status is not None:
                campos.append("status = %s")
                valores.append(status)
            if data_prazo is not None:
                campos.append("data_prazo = %s")
                valores.append(data_prazo)
            if nota is not None:
                campos.append("nota = %s")
                valores.append(nota)

            valores.append(id_tarefa)

            sql = f'''
            UPDATE tb_tarefa
            SET {", ".join(campos)}
            WHERE id_tarefa = %s
            '''

            conectar = self.conectar()
            if conectar is None:
                return False
            else:
                dados = conectar.cursor()
                dados.execute(sql, tuple(valores))
                conectar.commit()
                return True
        except Error as e:
            print(f"Erro ao alterar tarefa: {e}")
            return False

    # Método excluir tarefa
    def excluir(self, id_tarefa):
        try:
            self.set_id_tarefa(id_tarefa)
            sql = 'DELETE FROM tb_tarefa WHERE id_tarefa=%s'

            conectar = self.conectar()
            if conectar is None:
                return False
            else:
                dados = conectar.cursor()
                dados.execute(sql, (self.get_id_tarefa(),))
                conectar.commit()
                return True
        except Error as e:
            print(f"Erro ao excluir tarefa: {e}")
            return False

    # Método consultar tarefas por ID ou título
    def consultar(self, id_tarefa=None, titulo=None):
        try:
            conexao = self.conectar()
            if conexao is None:
                return False
            
            if id_tarefa is not None:
                sql = '''
                SELECT id_tarefa, titulo, descricao, categoria, status, data_prazo, nota
                FROM tb_tarefa
                WHERE id_tarefa = %s
                '''
                dados = conexao.cursor()
                dados.execute(sql, (id_tarefa,))
            elif titulo is not None:
                sql = '''
                SELECT id_tarefa, titulo, descricao, categoria, status, data_prazo, nota
                FROM tb_tarefa
                WHERE titulo LIKE %s
                '''
                dados = conexao.cursor()
                dados.execute(sql, ('%' + titulo + '%',))
            else:
                sql = '''
                SELECT id_tarefa, titulo, descricao, categoria, status, data_prazo, nota
                FROM tb_tarefa
                '''
                dados = conexao.cursor()
                dados.execute(sql)

            resultado = dados.fetchall()
            return resultado
        except Error as e:
            print(f"Erro ao consultar: {e}")
            return False
        finally:
            if conexao:
                conexao.close()

    # Consultar tarefas por status
    def consultar_por_status(self, status):
        try:
            conexao = self.conectar()
            if conexao is None:
                return False

            sql = '''
            SELECT id_tarefa, titulo, descricao, categoria, status, data_prazo, nota
            FROM tb_tarefa
            WHERE status = %s
            '''
            dados = conexao.cursor()
            dados.execute(sql, (status,))
            resultado = dados.fetchall()
            return resultado
        except Error as e:
            print(f"Erro ao consultar por status: {e}")
            return False
        finally:
            if conexao:
                conexao.close()

    # Consultar tarefas vencidas
    def consultar_vencidas(self, data_atual):
        try:
            conexao = self.conectar()
            if conexao is None:
                return False

            sql = '''
            SELECT id_tarefa, titulo, descricao, categoria, status, data_prazo, nota
            FROM tb_tarefa
            WHERE data_prazo < %s AND status != 'Concluída'
            '''
            dados = conexao.cursor()
            dados.execute(sql, (data_atual,))
            resultado = dados.fetchall()
            return resultado
        except Error as e:
            print(f"Erro ao consultar tarefas vencidas: {e}")
            return False
        finally:
            if conexao:
                conexao.close()


