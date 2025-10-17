from PyQt6 import QtCore, QtGui, QtWidgets
from conect_banco import adicionar_professo_no_conselho, mostrar_conselho, mostrar_membros_all

class Ui_adicionar_conselho(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.nome_selecionado = ""   # 🔹 inicializa para evitar erro
        self.dicionario_nome_id = {}
        self.parent=parent # 🔹 inicializa o dicionário
        self.setupUi(self)

    def setupUi(self, Widget):
        Widget.setObjectName("membros_inicial")
        Widget.resize(728, 289)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        Widget.setSizePolicy(sizePolicy)

        self.layoutWidget = QtWidgets.QWidget(parent=Widget)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 20, 581, 302))
        self.layoutWidget.setObjectName("layoutWidget")

        self.Layout_principal = QtWidgets.QVBoxLayout(Widget)
        self.Layout_principal.setContentsMargins(0, 0, 0, 0)
        self.Layout_principal.setObjectName("Layout_principal")

        # 🔹 Título
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.Layout_principal.addWidget(self.label)

        # 🔹 Linha de pesquisa
        self.Layout_pesquisar = QtWidgets.QHBoxLayout()
        self.comboBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.Layout_pesquisar.addWidget(self.comboBox)

        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.Layout_pesquisar.addWidget(self.lineEdit)

        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.Layout_pesquisar.addWidget(self.pushButton)
        self.Layout_principal.addLayout(self.Layout_pesquisar)

        # 🔹 Lista de membros
        self.layout_list_adicionar = QtWidgets.QHBoxLayout()
        self.layout_texto_integrantes = QtWidgets.QVBoxLayout()
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout_texto_integrantes.addWidget(self.label_2)
        self.layout_list_adicionar.addLayout(self.layout_texto_integrantes)

        self.listWidget = QtWidgets.QListWidget(parent=self.layoutWidget)
        self.layout_list_adicionar.addWidget(self.listWidget)

        spacer=QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.layout_list_adicionar.addItem(spacer)
        self.Layout_principal.addLayout(self.layout_list_adicionar)

        # 🔹 Botão salvar
        self.Layou_botao_salvar = QtWidgets.QHBoxLayout()
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFixedSize(100, 25)
        self.Layou_botao_salvar.addWidget(self.pushButton_3)
        self.Layout_principal.addLayout(self.Layou_botao_salvar)

        # 🔹 Conexões
        self.pushButton.clicked.connect(self.buscar)
        self.pushButton_3.clicked.connect(self.inserir_conselho)
        self.listWidget.clicked.connect(self.mostrar_item_selecionao)

        # 🔹 Inicializa a lista chamando carregar_membros
        self.carregar_membros()

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.label.setText(_translate("Widget", "Adicionar Integrante em Conselho"))
        self.comboBox.addItems(["NOME", "IDENTIDADE", "CPF"])
        self.pushButton.setText(_translate("Widget", "BUSCAR"))
        self.label_2.setText(_translate("Widget", "Integrantes"))
        self.pushButton_3.setText(_translate("Widget", "Adicionar"))

    def mostrar_item_selecionao(self):
        item = self.listWidget.currentItem()
        if item:
            self.nome_selecionado = item.text()

    def inserir_conselho(self):
        msg = QtWidgets.QMessageBox()

        if not self.nome_selecionado:
            msg.setWindowTitle("ERRO")
            msg.setText("Selecione um Professo")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.exec()
            return

        membros_conselho = mostrar_conselho()
        id_selecionado = self.dicionario_nome_id.get(self.nome_selecionado)

        if not id_selecionado:
            msg.setWindowTitle("Erro")
            msg.setText("Erro interno: id não encontrado.")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.exec()
            return

        # 🔹 Verifica se já está no conselho
        if id_selecionado in [info['id_professo'] for info in membros_conselho.values()]:
            msg.setWindowTitle("Aviso")
            msg.setText("Este professo já está no Conselho.")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()
            return

        # 🔹 Adiciona se não estiver
        retorno = adicionar_professo_no_conselho(id_professo=id_selecionado)
        if retorno:
            msg.setWindowTitle("Sucesso")
            msg.setText("Cadastro efetuado com sucesso")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.exec()
            self.carregar_membros()  # atualiza a lista
            self.nome_selecionado = ""  # 🔹 limpa seleção
            if self.parent:
                self.parent.conselho_janela()
        else:
            msg.setWindowTitle("Erro")
            msg.setText("Erro ao cadastrar professo")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.exec()

    def carregar_membros(self):
        self.listWidget.clear()
        membros = mostrar_membros_all(estado='Professo')
        membros_conselho = mostrar_conselho()

        ids_conselho = [dados['id_professo'] for dados in membros_conselho.values()]

        membros_disponiveis = {
            id_membro: dados for id_membro, dados in membros.items()
            if id_membro not in ids_conselho and dados['ativo'] == 'sim'
        }

        self.dicionario_nome_id = {
            dados['nome']: id_membro for id_membro, dados in membros_disponiveis.items()
        }

        for i, nome in enumerate(self.dicionario_nome_id.keys()):
            self.listWidget.insertItem(i, nome)

    def buscar(self):
        criterio = self.comboBox.currentText().lower()
        termo = self.lineEdit.text().strip().lower()

        if not termo:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setWindowTitle("Aviso")
            msg.setText("Digite algo para pesquisar.")
            msg.exec()
            return

        membros = mostrar_membros_all(estado='Professo')
        filtrados = {}
        for nome, id_membro in self.dicionario_nome_id.items():
            if termo in str(membros[id_membro][criterio]).lower():
                filtrados[nome] = id_membro

        self.listWidget.clear()
        for i, nome in enumerate(filtrados.keys()):
            self.listWidget.insertItem(i, nome)

        self.dicionario_nome_id = filtrados


