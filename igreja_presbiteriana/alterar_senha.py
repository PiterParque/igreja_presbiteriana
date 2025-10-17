from PyQt6 import QtCore, QtGui, QtWidgets
from conect_banco import alterar_senha_usuario

class ui_alterar_senha(QtWidgets.QWidget):
    def __init__(self, nome_usuario,id_usuario,senha_atual):
        super().__init__()
        self.nome_usuario=nome_usuario
        self.id_usuario=id_usuario
        self.senha_atual=senha_atual
        self.setupUi(self)
    def setupUi(self, Widget):
        Widget.setObjectName("alterar_senha")
        Widget.resize(516, 114)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        # ---- Título ----
        self.label_3 = QtWidgets.QLabel("Alteração de Senha", parent=Widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3.addWidget(self.label_3)

        # ---- Campos de senha ----
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.verticalLayout_labels = QtWidgets.QVBoxLayout()
        self.verticalLayout_inputs = QtWidgets.QVBoxLayout()

        font_label = QtGui.QFont()
        font_label.setPointSize(12)
        font_label.setBold(True)

        self.label_nova = QtWidgets.QLabel("NOVA SENHA", parent=Widget)
        self.label_nova.setFont(font_label)
        self.label_confirmar = QtWidgets.QLabel("CONFIRME A SENHA", parent=Widget)
        self.label_confirmar.setFont(font_label)
        self.verticalLayout_labels.addWidget(self.label_nova)
        self.verticalLayout_labels.addWidget(self.label_confirmar)

        self.entrada_nova_senha = QtWidgets.QLineEdit(parent=Widget)
        self.entrada_nova_senha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.entrada_confirmar_senha = QtWidgets.QLineEdit(parent=Widget)
        self.entrada_confirmar_senha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.verticalLayout_inputs.addWidget(self.entrada_nova_senha)
        self.verticalLayout_inputs.addWidget(self.entrada_confirmar_senha)

        self.horizontalLayout.addLayout(self.verticalLayout_labels)
        self.horizontalLayout.addLayout(self.verticalLayout_inputs)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        # ---- Botão SALVAR ----
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton("SALVAR", parent=Widget)
        self.pushButton.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
            )
        )
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        QtCore.QMetaObject.connectSlotsByName(Widget)
        self.pushButton.clicked.connect(self.salvar)
    def salvar(self):
        nova_senha = self.entrada_nova_senha.text()
        confirmar_senha = self.entrada_confirmar_senha.text()

        if not nova_senha or not confirmar_senha:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setText("Por favor, preencha todos os campos.")
            msg.setWindowTitle("Campos Incompletos")
            msg.exec()
            return

        if nova_senha != confirmar_senha:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.setText("As senhas não coincidem. Tente novamente.")
            msg.setWindowTitle("Erro de Senha")
            msg.exec()
            return

        sucesso = alterar_senha_usuario(id_usuario=self.id_usuario,nome_usuario=self.nome_usuario,nova_senha=nova_senha,senha_atual=self.senha_atual)
        if sucesso:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText("Senha alterada com sucesso!")
            msg.setWindowTitle("Sucesso")
            msg.exec()
            self.close()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setText("Falha ao alterar a senha. Tente novamente.")
            msg.setWindowTitle("Erro")
            msg.exec()


