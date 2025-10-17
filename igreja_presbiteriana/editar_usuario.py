from PyQt6 import QtCore, QtGui, QtWidgets
from conect_banco import editar_usuario, buscar_permissoes, definir_permissoes
from alterar_senha import ui_alterar_senha


class Ui_editar_usuario(QtWidgets.QWidget):
    def __init__(self, parent=None, usuario=None):
        super().__init__(parent)
        self.usuario = usuario
        self.setupUi(self)
        if self.usuario:
            self.carregar_dados_usuario()

    def setupUi(self, Form):
        Form.setObjectName("widget_informacso_usuario")
        Form.resize(450, 380)

        self.verticalLayout_7 = QtWidgets.QVBoxLayout(Form)

        # ---- Título ----
        self.label_11 = QtWidgets.QLabel("Editar Informações de Usuário", objectName="titulo_informacoes")
        font_titulo = QtGui.QFont()
        font_titulo.setPointSize(14)
        font_titulo.setBold(True)
        self.label_11.setFont(font_titulo)
        self.verticalLayout_7.addWidget(self.label_11)

        font_label = QtGui.QFont()
        font_label.setPointSize(12)
        font_label.setBold(True)

        # ---- Nome ----
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.label_4 = QtWidgets.QLabel("NOME", objectName="label_4")
        self.label_4.setFont(font_label)
        self.entrada_nome = QtWidgets.QLineEdit(objectName="entrada_nome")
        self.horizontalLayout.addWidget(self.label_4)
        self.horizontalLayout.addWidget(self.entrada_nome)
        self.verticalLayout_7.addLayout(self.horizontalLayout)

        # ---- Senha ----
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.label_12 = QtWidgets.QLabel("SENHA", objectName="label_12")
        self.label_12.setFont(font_label)
        self.alterar_senha = QtWidgets.QPushButton("ALTERAR SENHA", objectName="alterar_senha")
        self.alterar_senha.clicked.connect(self.alterar_senha_)
        self.horizontalLayout_5.addWidget(self.label_12)
        self.horizontalLayout_5.addWidget(self.alterar_senha)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        # ---- Tipo de Usuário ----
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.label_5 = QtWidgets.QLabel("TIPO DE USUÁRIO", objectName="label_5")
        self.label_5.setFont(font_label)
        self.tipo_usuario = QtWidgets.QComboBox(objectName="tipo_usuario")
        self.tipo_usuario.addItems(["COMUM","ADMINISTRADOR"])
        self.tipo_usuario.currentTextChanged.connect(self.acesso_administrador_comum)
        self.horizontalLayout_2.addWidget(self.label_5)
        self.horizontalLayout_2.addWidget(self.tipo_usuario)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        # ---- Data de Criação ----
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.label_6 = QtWidgets.QLabel("DATA DE CRIAÇÃO", objectName="label_6")
        self.label_6.setFont(font_label)
        self.entrada_data_criacao = QtWidgets.QDateEdit(objectName="entrada_data_criacao")
        self.entrada_data_criacao.setDisplayFormat("dd/MM/yyyy")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.horizontalLayout_3.addWidget(self.entrada_data_criacao)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        # ---- Ativo ----
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.label_13 = QtWidgets.QLabel("ATIVO", objectName="label_13")
        self.label_13.setFont(font_label)
        self.sim_ativo = QtWidgets.QRadioButton("Sim", objectName="sim_ativo")
        self.nao_ativo = QtWidgets.QRadioButton("Não", objectName="nao_ativo")
        self.sim_ativo.setChecked(True)
        self.horizontalLayout_6.addWidget(self.label_13)
        self.horizontalLayout_6.addWidget(self.sim_ativo)
        self.horizontalLayout_6.addWidget(self.nao_ativo)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        # ---- Widget de acessos ----
        widget_acessos = QtWidgets.QWidget(parent=Form)
        widget_acessos.setObjectName("widget_acessos")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(widget_acessos)

        self.label = QtWidgets.QLabel("ACESSOS", widget_acessos)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_5.addLayout(self.verticalLayout)

        labels_info = [
            ("FINANÇAS", 10),
            ("Cadastro de membros", 10),
            ("Gestão de Função", 10),
            ("Gestão de  Usuarios", 10)
        ]
        for text, size in labels_info:
            lbl = QtWidgets.QLabel(text, widget_acessos)
            f = QtGui.QFont()
            f.setPointSize(size)
            f.setBold(True)
            lbl.setFont(f)
            self.verticalLayout.addWidget(lbl)

        # ---- RadioButtons ----
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        radios = [
            ("sim_financas", "SIM", "nao_financas", "NÃO"),
            ("sim_cadastro_membros", "SIM", "nao_cadastro_membros", "NÃO"),
            ("sim_gestao_funcoes", "SIM", "nao_gestao_funcoes", "NÃO"),
            ("sim_gestao_usuarios", "SIM", "nao_gestao_usuarios", "NÃO")
        ]

        for sim_name, sim_text, nao_name, nao_text in radios:
            h_layout = QtWidgets.QHBoxLayout()

            sim_rb = QtWidgets.QRadioButton(sim_text, widget_acessos)
            sim_rb.setObjectName(sim_name)
            font_rb = QtGui.QFont()
            font_rb.setBold(True)
            sim_rb.setFont(font_rb)

            nao_rb = QtWidgets.QRadioButton(nao_text, widget_acessos)
            nao_rb.setObjectName(nao_name)
            nao_rb.setFont(font_rb)
            nao_rb.setChecked(True)

            grupo = QtWidgets.QButtonGroup(widget_acessos)
            grupo.addButton(sim_rb)
            grupo.addButton(nao_rb)

            h_layout.addWidget(sim_rb)
            h_layout.addWidget(nao_rb)
            self.verticalLayout_2.addLayout(h_layout)

        self.verticalLayout_7.addWidget(widget_acessos)

        # ---- Botão Salvar ----
        self.btn_salvar = QtWidgets.QPushButton("SALVAR", objectName="btn_salvar")
        font_btn = QtGui.QFont()
        font_btn.setBold(True)
        font_btn.setPointSize(12)
        self.btn_salvar.setFont(font_btn)
        self.btn_salvar.setStyleSheet("background-color: rgb(4,64,22); color: white; border-radius: 8px; padding: 6px;")
        self.verticalLayout_7.addWidget(self.btn_salvar, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.btn_salvar.clicked.connect(self.salvar_usuario)
    
        # Ajusta visibilidade de campos conforme tipo de usuário
        self.acesso_administrador_comum()

    def carregar_dados_usuario(self):
        self.entrada_nome.setText(self.usuario.get("nome", ""))
        tipo = "ADMINISTRADOR" if self.usuario.get("tipo_usuario", "").lower() == "admin" else "COMUM"
        self.tipo_usuario.setCurrentText(tipo)
        data = QtCore.QDate.fromString(
            self.usuario.get("data_entrada", QtCore.QDate.currentDate().toString("yyyy-MM-dd")),
            "yyyy-MM-dd"
        )
        self.entrada_data_criacao.setDate(data if data.isValid() else QtCore.QDate.currentDate())

        ativo = self.usuario.get("ativo", "sim").lower()
        self.sim_ativo.setChecked(ativo == "sim")
        self.nao_ativo.setChecked(ativo == "nao")

        permissoes = buscar_permissoes(id_usuario=self.usuario["id"])
        if permissoes:
            self.findChild(QtWidgets.QRadioButton, "sim_financas").setChecked(permissoes["financa"])
            self.findChild(QtWidgets.QRadioButton, "nao_financas").setChecked(not permissoes["financa"])
            self.findChild(QtWidgets.QRadioButton, "sim_cadastro_membros").setChecked(permissoes["gestao_membros"])
            self.findChild(QtWidgets.QRadioButton, "nao_cadastro_membros").setChecked(not permissoes["gestao_membros"])
            self.findChild(QtWidgets.QRadioButton, "sim_gestao_funcoes").setChecked(permissoes["gestao_funcoes"])
            self.findChild(QtWidgets.QRadioButton, "nao_gestao_funcoes").setChecked(not permissoes["gestao_funcoes"])
            self.findChild(QtWidgets.QRadioButton, "sim_gestao_usuarios").setChecked(permissoes["gestao_usuarios"])
            self.findChild(QtWidgets.QRadioButton, "nao_gestao_usuarios").setChecked(not permissoes["gestao_usuarios"])

    def salvar_usuario(self):
        nome = self.entrada_nome.text().strip()
        tipo_usuario = "admin" if self.tipo_usuario.currentText() == "ADMINISTRADOR" else "comum"
        ativo = self.sim_ativo.isChecked()
        data_criacao = self.entrada_data_criacao.date().toString("yyyy-MM-dd")

        if not nome:
            QtWidgets.QMessageBox.warning(self, "Atenção", "Nome é obrigatório!")
            return

        # Atualiza usuário
        editar_usuario(self.usuario["id"], nome, tipo_usuario, data_criacao, ativo)

        # Atualiza permissões
        alterar_permissoes = {
            "financa": self.findChild(QtWidgets.QRadioButton, "sim_financas").isChecked(),
            "gestao_membros": self.findChild(QtWidgets.QRadioButton, "sim_cadastro_membros").isChecked(),
            "gestao_funcoes": self.findChild(QtWidgets.QRadioButton, "sim_gestao_funcoes").isChecked(),
            "gestao_usuarios": self.findChild(QtWidgets.QRadioButton, "sim_gestao_usuarios").isChecked()
        }

        definir_permissoes(
            id_usuario=self.usuario["id"],
            nome_usuario=nome,
            id_permissor=1,
            nome_permissor="ADMIN",
            financa=alterar_permissoes["financa"],
            gestao_membros=alterar_permissoes["gestao_membros"],
            gestao_funcoes=alterar_permissoes["gestao_funcoes"],
            gestao_usuarios=alterar_permissoes["gestao_usuarios"]
            
            
        )

        QtWidgets.QMessageBox.information(self, "Sucesso", f"Usuário {nome} atualizado com sucesso!")
        self.close()

    def alterar_senha_(self):
        self.alterar_senha_ui = ui_alterar_senha(
            nome_usuario=self.usuario["nome"],
            id_usuario=self.usuario["id"],
            senha_atual=self.usuario.get('senha', '')
        )
        self.alterar_senha_ui.show()

    def acesso_administrador_comum(self):
        gestao_usuarios_rbs = [
            self.findChild(QtWidgets.QRadioButton, "sim_gestao_usuarios"),
            self.findChild(QtWidgets.QRadioButton, "nao_gestao_usuarios")
        ]
        if self.tipo_usuario.currentText() == "ADMINISTRADOR":
            for rb in gestao_usuarios_rbs:
                if rb:
                    rb.setEnabled(True)
        else:
            for rb in gestao_usuarios_rbs:
                if rb:
                    rb.setEnabled(False)
                    if "nao_" in rb.objectName():
                        rb.setChecked(True)


