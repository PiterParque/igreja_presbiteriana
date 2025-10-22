
import sqlite3
import os
import tempfile
import webbrowser
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QFileDialog,
    QVBoxLayout, QMessageBox, QListWidget
)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciar PDFs no SQLite")
        self.setGeometry(200, 200, 500, 300)

        # Layout
        layout = QVBoxLayout()

        # Botão salvar PDF
        self.btn_salvar = QPushButton("Selecionar e Salvar PDF")
        self.btn_salvar.clicked.connect(self.selecionar_pdf)
        layout.addWidget(self.btn_salvar)

        # Lista para mostrar PDFs salvos
        self.lista = QListWidget()
        self.lista.itemDoubleClicked.connect(self.abrir_pdf)
        layout.addWidget(self.lista)

        # Botão para atualizar lista
        self.btn_listar = QPushButton("Atualizar Lista de PDFs")
        self.btn_listar.clicked.connect(self.listar_pdfs)
        layout.addWidget(self.btn_listar)

        self.setLayout(layout)

        # Criar banco/tabela se não existir
        self.init_db()
        self.listar_pdfs()

    def init_db(self):
        con = sqlite3.connect("arquivos.db")
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                pdf BLOB
            )
        """)
        con.commit()
        con.close()

    def selecionar_pdf(self):
        # Abre explorador de arquivos
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecione um PDF", "", "Arquivos PDF (*.pdf)")
        
        if arquivo:
            try:
                with open(arquivo, "rb") as f:
                    pdf_data = f.read()

                nome_arquivo = os.path.basename(arquivo)

                con = sqlite3.connect("arquivos.db")
                cur = con.cursor()
                cur.execute("INSERT INTO documentos (nome, pdf) VALUES (?, ?)", (nome_arquivo, pdf_data))
                con.commit()
                con.close()

                QMessageBox.information(self, "Sucesso", f"PDF '{nome_arquivo}' salvo no banco com sucesso!")
                self.listar_pdfs()
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))

    def listar_pdfs(self):
        self.lista.clear()
        con = sqlite3.connect("arquivos.db")
        cur = con.cursor()
        cur.execute("SELECT id, nome FROM documentos")
        for row in cur.fetchall():
            self.lista.addItem(f"{row[0]} - {row[1]}")
        con.close()

    def abrir_pdf(self, item):
        try:
            # Pegar ID do item selecionado
            id_doc = int(item.text().split(" - ")[0])

            con = sqlite3.connect("arquivos.db")
            cur = con.cursor()
            cur.execute("SELECT nome, pdf FROM documentos WHERE id=?", (id_doc,))
            row = cur.fetchone()
            con.close()

            if row:
                nome, pdf_data = row
                # Criar arquivo temporário
                temp_path = os.path.join(tempfile.gettempdir(), nome)
                with open(temp_path, "wb") as f:
                    f.write(pdf_data)

                # Abrir no visualizador padrão
                webbrowser.open(temp_path)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))



