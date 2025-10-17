from PyQt6 import QtCore, QtGui, QtWidgets
from conect_banco import (
    mostrar_membros_all,
    cadastrar_funcao,
    buscar_funcoes_por_area
)


class ui_adicionar_funcao(QtWidgets.QWidget):
    def __init__(self, area=str,parent=None):
        super().__init__()
        self.area = area
        self.parent=parent
        self.setupUi(self)

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(590, 380)
        self.widget = QtWidgets.QWidget(parent=Widget)
        self.widget.setGeometry(QtCore.QRect(30, 30, 520, 320))
        self.widget.setObjectName("widget")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # ======= TÍTULO =======
        self.label = QtWidgets.QLabel(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)

        # ======= CAMPO DE PESQUISA =======
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lineEdit = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit.setPlaceholderText("Digite o nome para pesquisar...")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        # ======= LAYOUT PRINCIPAL =======
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        # ---- Lista de integrantes ----
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)

        self.listWidget = QtWidgets.QListWidget(parent=self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)

        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        # ---- Área de detalhes ----
        self.widget1 = QtWidgets.QWidget(parent=self.widget)
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setObjectName("verticalLayout")

        # Nome
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.widget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.lineEdit_2.setReadOnly(True)


        # Função
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(parent=self.widget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)

        self.lineEdit_funcao = QtWidgets.QLineEdit(parent=self.widget1)
        self.lineEdit_funcao.setPlaceholderText("Digite a função do membro...")
        self.lineEdit_funcao.setObjectName("lineEdit_funcao")
        self.horizontalLayout_3.addWidget(self.lineEdit_funcao)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        # Data de entrada
        self.horizontalLayout_data = QtWidgets.QHBoxLayout()
        self.horizontalLayout_data.setObjectName("horizontalLayout_data")
        self.label_data = QtWidgets.QLabel(parent=self.widget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_data.setFont(font)
        self.label_data.setText("Data de Entrada:")
        self.horizontalLayout_data.addWidget(self.label_data)

        self.dateEdit = QtWidgets.QDateEdit(parent=self.widget1)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.dateEdit.setObjectName("dateEdit")
        self.horizontalLayout_data.addWidget(self.dateEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_data)

        # Botão adicionar
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.widget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5.addWidget(self.widget1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.spacer = QtWidgets.QSpacerItem(
            300, 500, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.horizontalLayout_5.addItem(self.spacer)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

        # ======= Conexões =======
        self.listWidget.itemClicked.connect(self.mostrar_membro_clicado)

        self.pushButton_2.clicked.connect(self.adicionar_membro_area)

        # Carrega tabela inicial
        self.prencher_tabela()

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Adicionar Função "))
        self.label.setText(_translate("Widget", "Adicionar Membros para "+self.area))
        self.pushButton.setText(_translate("Widget", "Pesquisar"))
        self.label_2.setText(_translate("Widget", "Lista de integrantes"))
        self.label_3.setText(_translate("Widget", "Nome:"))
        self.label_4.setText(_translate("Widget", "Função"))
        self.pushButton_2.setText(_translate("Widget", "Adicionar"))
        self.widget1.setVisible(False)
        self.pushButton.clicked.connect(self.pesquisar)

        

    # ============================
    #       FUNÇÕES
    # ============================

    def mostrar_membro_clicado(self):
        """Exibe a área de detalhes quando um nome é clicado."""
        self.widget1.setVisible(True)
        self.spacer.changeSize(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.horizontalLayout_5.update()
        self.lineEdit_2.setText(self.listWidget.currentItem().text())
        
    def prencher_tabela(self):
        """Preenche a lista com os membros da área."""
        self.listWidget.clear()
        membros = mostrar_membros_all(estado="Professo")
        membros_area = buscar_funcoes_por_area(area=self.area)

        for membro in membros.keys():
            nome = membros[membro]['nome']
            if membro not in membros_area.keys():
                    item = QtWidgets.QListWidgetItem(str(nome))
                    self.listWidget.addItem(item)
    
    def adicionar_membro_area(self):
        """Adiciona o membro selecionado à área."""
        nome = self.lineEdit_2.text().strip()
        funcao = self.lineEdit_funcao.text().strip()
        data_entrada = self.dateEdit.date().toString("dd/MM/yyyy")

        if not nome or not funcao:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Preencha o nome e a função.")
            return

        membros = mostrar_membros_all(estado="Professo")
        membro_id = None
        for id_, dados in membros.items():
            if dados['nome'].lower() == nome.lower():
                membro_id = id_
                break

        if membro_id is None:
            QtWidgets.QMessageBox.critical(self, "Erro", "Membro não encontrado no banco.")
            return

        sucesso = cadastrar_funcao(
            id_membro=membro_id,
            nome=nome,
            area=self.area,
            funcao=funcao,
            data_entrada=data_entrada
        )

        if sucesso:
            QtWidgets.QMessageBox.information(self, "Sucesso", f"{nome} adicionado à área {self.area}.")
            self.widget1.setVisible(False)
            self.prencher_tabela()
            if self.parent:
                 self.parent.ver_membros()
        else:
            QtWidgets.QMessageBox.critical(self, "Erro", "Falha ao cadastrar o membro.")
    def pesquisar(self):
        """Filtra os membros pelo nome digitado no campo de pesquisa."""
        texto_busca = self.lineEdit.text().strip().lower()
        self.listWidget.clear()

        # Carrega todos os membros e os já vinculados à área
        membros = mostrar_membros_all(estado="Professo")
        membros_area = buscar_funcoes_por_area(area=self.area)

        # Filtra apenas os membros que ainda não estão na área
        for membro_id, dados in membros.items():
            nome = dados['nome']
            if membro_id not in membros_area.keys():
                # Se o campo estiver vazio, mostra todos
                # Se não, mostra apenas quem contém o texto buscado
                if not texto_busca or texto_busca in nome.lower():
                    item = QtWidgets.QListWidgetItem(str(nome))
                    self.listWidget.addItem(item)

        # Caso nenhum resultado seja encontrado
        if self.listWidget.count() == 0:
            self.listWidget.addItem("Nenhum membro encontrado.")




