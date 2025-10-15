from PyQt6 import QtCore, QtGui, QtWidgets
from conect_banco import editar_funcao

class Ui_EditarMembro(QtWidgets.QWidget):
    def __init__(self, membro, area,parent=None):
        """
        membro: dicionário com informações do membro selecionado
        area: nome da área (ex: 'LOUVOR')
        """
        super().__init__()
        self.membro = membro
        self.area = area
        self.parent=parent
        self.membro=membro
        self.setupUi(self)

    def setupUi(self, Widget):
        Widget.setObjectName("EditarMembro")
        Widget.resize(420, 250)
        Widget.setWindowTitle("Editar Membro")

        # Layout principal
        self.verticalLayout = QtWidgets.QVBoxLayout(Widget)

        # ===== Campo Nome =====
        self.label_nome = QtWidgets.QLabel("Nome:")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_nome.setFont(font)
        self.verticalLayout.addWidget(self.label_nome)

        self.lineEdit_nome = QtWidgets.QLineEdit()
        self.lineEdit_nome.setPlaceholderText("Digite o nome do membro")
        self.verticalLayout.addWidget(self.lineEdit_nome)

        # ===== Campo Função =====
        self.label_funcao = QtWidgets.QLabel("Função:")
        self.label_funcao.setFont(font)
        self.verticalLayout.addWidget(self.label_funcao)

        self.lineEdit_funcao = QtWidgets.QLineEdit()
        self.lineEdit_funcao.setPlaceholderText("Digite a função do membro")
        self.verticalLayout.addWidget(self.lineEdit_funcao)

        # ===== Campo Data =====
        self.label_data = QtWidgets.QLabel("Data de Entrada:")
        self.label_data.setFont(font)
        self.verticalLayout.addWidget(self.label_data)

        self.dateEdit = QtWidgets.QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.verticalLayout.addWidget(self.dateEdit)

        # ===== Botões =====
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.pushButton_salvar = QtWidgets.QPushButton("Salvar")
        self.pushButton_cancelar = QtWidgets.QPushButton("Cancelar")
        self.horizontalLayout.addWidget(self.pushButton_salvar)
        self.horizontalLayout.addWidget(self.pushButton_cancelar)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # ===== Conexões =====
        self.pushButton_salvar.clicked.connect(self.salvar_alteracoes)
        self.pushButton_cancelar.clicked.connect(self.close)
        
        # ===== Pré-preenche se houver membro =====
        if self.membro:
            self.preencher_campos()
        self.lineEdit_nome.setReadOnly(True)

    def preencher_campos(self):
        """Preenche os campos com os dados do membro recebido."""
        self.lineEdit_nome.setText(self.membro.get('nome', ''))
        self.lineEdit_funcao.setText(self.membro.get('funcao', ''))
        try:
            data = QtCore.QDate.fromString(self.membro.get('data_entrada', ''), "yyyy-MM-dd")
            if data.isValid():
                self.dateEdit.setDate(data)
        except Exception:
            pass

    def salvar_alteracoes(self):
        """Salva as alterações no banco."""
        nome = self.lineEdit_nome.text().strip()
        funcao = self.lineEdit_funcao.text().strip()
        data_entrada = self.dateEdit.date().toString("yyyy-MM-dd")

        if not nome or not funcao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")
            return

        try:
            editar_funcao(
                id_membro=self.membro['id_membro'],
                nome=nome,
                area=self.area,
                funcao=funcao,
                data_entrada=data_entrada,
                id_funcao=self.membro['id']
            )
            QtWidgets.QMessageBox.information(self, "Sucesso", "Dados atualizados com sucesso!")
            self.close()
            if self.parent:
                 self.parent.ver_membros()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao salvar alterações:\n{e}")
