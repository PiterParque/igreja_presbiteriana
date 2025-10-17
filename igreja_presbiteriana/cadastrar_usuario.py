from PyQt6 import QtCore, QtGui, QtWidgets
from conect_banco import cadastrar_usuario

class Ui_CriarUsuario(QtWidgets.QWidget):
    def __init__(self, parent=None, usuario=None):
        super().__init__()
        self.parent = parent
        self.usuario = usuario
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("widget_informacso_usuario")
        Form.resize(450, 220)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(Form)

        # ---- Título ----
        self.label_11 = QtWidgets.QLabel("Informações de Usuário", objectName="titulo_informacoes")
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
        self.entrada_senha = QtWidgets.QLineEdit(objectName="alterar_senha")
        self.entrada_senha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.horizontalLayout_5.addWidget(self.label_12)
        self.horizontalLayout_5.addWidget(self.entrada_senha)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        # ---- Confirmar Senha ----
        self.horizontalLayout_confirma = QtWidgets.QHBoxLayout()
        self.label_confirma = QtWidgets.QLabel("CONFIRMAR SENHA", objectName="label_confirma_senha")
        self.label_confirma.setFont(font_label)
        self.confirmar_senha = QtWidgets.QLineEdit(objectName="confirmar_senha")
        self.confirmar_senha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.horizontalLayout_confirma.addWidget(self.label_confirma)
        self.horizontalLayout_confirma.addWidget(self.confirmar_senha)
        self.verticalLayout_7.addLayout(self.horizontalLayout_confirma)

        # ---- Tipo ----
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.label_5 = QtWidgets.QLabel("TIPO DE USUÁRIO", objectName="label_5")
        self.label_5.setFont(font_label)
        self.tipo_usuario = QtWidgets.QComboBox(objectName="tipo_usuario")
        self.tipo_usuario.addItems(["COMUM", "ADMINISTRADOR"])
        self.horizontalLayout_2.addWidget(self.label_5)
        self.horizontalLayout_2.addWidget(self.tipo_usuario)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.tipo_usuario.currentTextChanged.connect(self.acesso_administrador_comum)

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

        # ---- Widget de Acessos ----
        self.widget_acessos = QtWidgets.QWidget(parent=Form)
        self.widget_acessos.setObjectName("widget_acessos")
        self.widget_acessos.resize(311, 158)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_acessos)

        # Linha vertical
        self.line = QtWidgets.QFrame(self.widget_acessos)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.verticalLayout_3.addWidget(self.line)

        # Título
        self.label = QtWidgets.QLabel("ACESSOS", self.widget_acessos)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.verticalLayout_3.addWidget(self.label)

        # Layout principal
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        # Labels das permissões
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        labels_info = [
            ("FINANÇAS", 10),
            ("Cadastro de membros", 10),
            ("Gestão de Função", 10),
            ("Gestão de  Usuarios", 10)
        ]
        for text, size in labels_info:
            lbl = QtWidgets.QLabel(text, self.widget_acessos)
            f = QtGui.QFont()
            f.setPointSize(size)
            f.setBold(True)
            lbl.setFont(f)
            self.verticalLayout.addWidget(lbl)

        # ---- RadioButtons ----
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        # Lista de permissões com seus objectNames
        radios = [
            ("sim_financas", "SIM", "nao_financas", "NÃO"),
            ("sim_cadastro_membros", "SIM", "nao_cadastro_membros", "NÃO"),
            ("sim_gestao_funcoes", "SIM", "nao_gestao_funcoes", "NÃO"),
            ("sim_gestao_usuarios", "SIM", "nao_gestao_usuarios", "NÃO")
        ]

        # Cria um grupo para cada linha de acesso e guarda referências como atributos
        self._button_groups = []
        for sim_name, sim_text, nao_name, nao_text in radios:
            h_layout = QtWidgets.QHBoxLayout()

            sim_rb = QtWidgets.QRadioButton(sim_text, self.widget_acessos)
            sim_rb.setObjectName(sim_name)
            font_rb = QtGui.QFont()
            font_rb.setBold(True)
            sim_rb.setFont(font_rb)

            nao_rb = QtWidgets.QRadioButton(nao_text, self.widget_acessos)
            nao_rb.setObjectName(nao_name)
            nao_rb.setFont(font_rb)
            nao_rb.setChecked(True)

            # guarda como atributo para poder acessar depois
            setattr(self, sim_name, sim_rb)
            setattr(self, nao_name, nao_rb)

            grupo = QtWidgets.QButtonGroup(self.widget_acessos)
            grupo.addButton(sim_rb)
            grupo.addButton(nao_rb)
            self._button_groups.append(grupo)

            h_layout.addWidget(sim_rb)
            h_layout.addWidget(nao_rb)
            self.verticalLayout_2.addLayout(h_layout)

        self.verticalLayout_7.addWidget(self.widget_acessos)

        # ---- Botão ----
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.SALVAR = QtWidgets.QPushButton("SALVAR", objectName="SALVAR")
        self.horizontalLayout_8.addWidget(self.SALVAR)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        # Conecta botão
        self.SALVAR.clicked.connect(self.salvar_usuario)

        # chama uma vez para ajustar estado inicial (agora aceita argumento opcional)
        self.acesso_administrador_comum()

    def salvar_usuario(self):
        nome = self.entrada_nome.text().strip()
        senha = self.entrada_senha.text()
        confirmar_senha = self.confirmar_senha.text()
        tipo_usuario = "admin" if self.tipo_usuario.currentText() == "ADMINISTRADOR" else "comum"
        ativo = True if self.sim_ativo.isChecked() else False
        nome_criador = "ADMIN"
        id_criador = 1

        if not nome or not senha:
            QtWidgets.QMessageBox.warning(self, "Atenção", "Nome e senha são obrigatórios!")
            return

        if senha != confirmar_senha:
            QtWidgets.QMessageBox.warning(self, "Atenção", "As senhas não coincidem!")
            return
                    # Pegar valores dos RadioButtons usando os atributos
        permissoes={}
        financas = getattr(self, "sim_financas").isChecked()
        cadastro_membros = getattr(self, "sim_cadastro_membros").isChecked()
        gestao_funcoes = getattr(self, "sim_gestao_funcoes").isChecked()
        gestao_usuarios = getattr(self, "sim_gestao_usuarios").isChecked()
        permissoes['financas']=financas
        permissoes['cadastro_membros']=cadastro_membros
        permissoes['gestao_funcoes']=gestao_funcoes
        permissoes['gestao_usuarios']=gestao_usuarios
        retorno=cadastrar_usuario(nome=nome, senha=senha, tipo_usuario=tipo_usuario,
                             nome_criador=nome_criador, id_criador=id_criador, ativo=ativo,permisoes=permissoes)
        print("permissoes da tela de cadastro:",permissoes)

        if retorno :
            QtWidgets.QMessageBox.information(self, "Sucesso", f"Usuário {nome} cadastrado com sucesso!")

            if self.parent:
                self.parent.atualizar_tabela()
        else:
            QtWidgets.QMessageBox.critical(self, "Erro", "Erro ao cadastrar usuário no banco de dados")

    def acesso_administrador_comum(self, _text=None):
        """Habilita/desabilita os rádios de gestão de usuários.
           Recebe um argumento opcional porque é conectado a currentTextChanged."""
        sim_rb = getattr(self, "sim_gestao_usuarios", None)
        nao_rb = getattr(self, "nao_gestao_usuarios", None)

        # se ainda não foram criados, sai (chamada inicial pode acontecer antes)
        if sim_rb is None or nao_rb is None:
            return

        if self.tipo_usuario.currentText() == "ADMINISTRADOR":
            sim_rb.setEnabled(True)
            nao_rb.setEnabled(True)
        else:
            sim_rb.setEnabled(False)
            nao_rb.setEnabled(False)
            nao_rb.setChecked(True)


