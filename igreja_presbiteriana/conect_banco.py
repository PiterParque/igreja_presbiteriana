import sqlite3
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QFileDialog, QMessageBox
# Verifica se o banco existe
db_path = 'igreja.db'
criar_tabelas = not os.path.exists(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
if criar_tabelas:
    cursor.execute("""
            CREATE TABLE saldo(
                id_saldo INTEGER PRIMARY KEY AUTOINCREMENT,
                DATA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                valor REAL
            );
        """)
    cursor.execute("""
            CREATE TABLE movimento_financeiro (
                id_movimento INTEGER PRIMARY KEY AUTOINCREMENT,
                data DATE,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                movimento boolean,
                tipo_movimento TEXT,
                valor REAL,
                obs TEXT
            );
        """)
    cursor.execute("""
        CREATE TABLE PROFESSOS(
            ID_PROFESSO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME TEXT,
            ENDERECO TEXT,
            DATA_PPFB DATE,
            DATA_NASC DATE,
            IDENTIDADE TEXT,
            CPF TEXT,
            TELEFONE TEXT,
            FORMA_ADMISSAO TEXT,
            GENERO TEXT,
            ATIVO BOOLEAN,
            DATA_CRIACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
    """)

    cursor.execute("""
        CREATE TABLE PROFESSOS_TRANSFERIDOS(
            ID_PROFESSO INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_PROFESSO_TRANSFERIDO INT ,
            IGREJA_ORIGEM TEXT,
            DATA_TRASNF DATE,
            CARTA BLOB
                    );
    """)
    cursor.execute("""
        CREATE TABLE MENORES(
            ID_MENOR INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME TEXT,
            NOME_PAI TEXT,
            NOME_MAE TEXT,
            RESPONSAVEL TEXT,
            TELEFONE_RESPONSAVEL TEXT,       
            DATA_NASC DATE,
            ATIVO BOOLEAN 
        );
    """)
    cursor.execute("""
        CREATE TABLE AGREGADOS(
            ID_AGREGADO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME TEXT,
            TELEFONE TEXT,
            ENDERECO TEXT,
            ATIVO BOOLEAN
        );
    """)
    cursor.execute("""
        CREATE TABLE JUNTA_DIAGONAL(
            ID_JUNTA INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_PROFESSO INTEGER,
            NOME TEXT,
            DATA_ENTRADA TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("""
        CREATE TABLE CONSELHO(
            ID_CONSELHO INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_PROFESSO INTEGER,
            DATA_ENTRADA TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """) 
    cursor.execute("""
        CREATE TABLE PROFESSOS_DESATIVADOS_ATIVADOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_PROFESSO INTEGER ,
            ATIVO BOOL,
            DATA TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
    """)
    cursor.execute("""
        CREATE TABLE MENORES_DESATIVADOS_ATIVADOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_MENOR INTEGER ,
            ATIVO BOOL,
            DATA TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
    """)
    cursor.execute("""
        CREATE TABLE AGREGADOS_DESATIVADOS_ATIVADOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_AGREGADO INTEGER ,
            ATIVO BOOL,
            DATA TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
    """)
    cursor.execute("""
        CREATE TABLE FUNCOES(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_MEMBRO INTEGER,
            NOME TEXT,
            AREA TEXT,
            FUNCAO TEXT,
            DATA_ENTRADA DATE
                    );
    """)
    cursor.execute("""
        CREATE TABLE USUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME TEXT,
            SENHA TEXT,
            tipo_usuario TEXT,
            DATA_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
            ID_CRIADOR INT,
            NOME_CRIADOR TEXT,
            ATIVO BOOL
                    );  
    """)
    cursor.execute("""
        CREATE TABLE PERMISSOES(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_USUARIO INT,
            NOME_USUARIO TEXT,     
            tipo_usuario TEXT,
            ID_USUARIO_P INT, --P=USUARIO QUE PERMITIU
            NOME_USUARIO_P TEXT,            
            DATA_PERMISSAO TEXT DEFAULT CURRENT_TIMESTAMP,
            FINANCA BOOL,
            GESTAO_MEMBROS BOOL,
            GESTAO_FUNCOES BOOL,
            GESTAO_USUARIOS BOOL      
                    );  
    """)
    cursor.execute("""
        CREATE TABLE VESICULOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            LIVRO TEXT,     
            VERSICULO TEXT,           
            DATA_CADASTRO TEXT DEFAULT CURRENT_TIMESTAMP
                    );  
    """)
    cursor.execute("""
        CREATE TABLE VESICULO_atual(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            LIVRO TEXT,     
            VERSICULO TEXT        
                    );  
    """)


    # Insere o saldo inicial se a tabela estiver vazia
    cursor.execute("INSERT INTO saldo (valor) VALUES(?)", ("0",))
    conn.commit()
    permissoes_teste = {
        'financas': 1,
        'cadastro_membros': 1,
        'gestao_funcoes': 1,
        'gestao_usuarios': 1
    }

    # Dados simulados do novo usuário
    nome_teste = "Administrador"
    senha_teste = "12345"
    tipo_usuario_teste = "Administrador"
    nome_criador_teste = "Sistema"
    id_criador_teste = 1
    ativo_teste = 1

    print(" Testando criação de usuário...")
    from conect_banco import cadastrar_usuario,inserir_versiculo_atual,cadastrar_vesiculo
    resultado = cadastrar_usuario(
        nome=nome_teste,
        senha=senha_teste,
        tipo_usuario=tipo_usuario_teste,
        nome_criador=nome_criador_teste,
        id_criador=id_criador_teste,
        ativo=ativo_teste,
        permisoes=permissoes_teste

    )

        # Inserir versículos de exemplo
    inserir_versiculo_atual("Filipenses 4:13", "Tudo posso naquele que me fortalece.")
    inserir_versiculo_atual("Salmos 23:1", "O Senhor é o meu pastor; nada me faltará.")
    inserir_versiculo_atual("Provérbios 3:5-6", "Confia no Senhor de todo o teu coração e não te apoies no teu próprio entendimento.")
    inserir_versiculo_atual("Isaías 41:10", "Não temas, porque eu sou contigo; eu te fortaleço e te ajudo.")
    inserir_versiculo_atual("João 3:16", "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito.")
    cadastrar_vesiculo("Salmos 23:1", "O Senhor é o meu pastor; nada me faltará.")
    cadastrar_vesiculo("Filipenses 4:13", "Tudo posso naquele que me fortalece.")
    cadastrar_vesiculo("Provérbios 3:5-6", "Confia no Senhor de todo o teu coração.")
    cadastrar_vesiculo("Isaías 41:10", "Não temas, porque eu sou contigo.")
    cadastrar_vesiculo("João 3:16", "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito.")
def movimento_financeiro(data, movimento, tipo_movimento, valor, obs, conexao=cursor):
    try:
        conexao.execute("SELECT valor FROM saldo ORDER BY id_saldo DESC LIMIT 1")
        valor_atual= conexao.fetchone()[0]
        if movimento == True:
            valor_atual=float(valor_atual)+float(valor)
            valor_atual=str(valor_atual)
            conexao.execute("INSERT INTO saldo (valor) VALUES(?)",(valor_atual,))
            conn.commit()
            conexao.execute("""
            INSERT INTO movimento_financeiro (data, movimento, tipo_movimento, valor, obs)
            VALUES (?, ?, ?, ?, ?)
            """, (data, movimento, tipo_movimento, valor, obs))
            conn.commit()
            return True
        else:
            valor_atual=float(valor_atual)-float(valor)
            if valor_atual < 0:
                return False
            else:
                print(movimento)
                valor_atual=str(valor_atual)
                conexao.execute("INSERT INTO saldo (valor) VALUES(?)",(valor_atual,))
                conn.commit()
                conexao.execute("""
                INSERT INTO movimento_financeiro (data, movimento, tipo_movimento, valor, obs)
                VALUES (?, ?, ?, ?, ?)
                """, (data, movimento, tipo_movimento, valor, obs))
                conn.commit()
                return True
        
    except Exception as e:
        print(f"Erro ao inserir movimento financeiro: {e}")
        return False
def valor_atual(conexao=cursor):
        conexao.execute("SELECT valor FROM saldo ORDER BY id_saldo DESC LIMIT 1")
        valor_atual= conexao.fetchone()
        return valor_atual
def saldo_por_data(data, conexao=cursor):
    """
    Retorna o saldo em uma data específica.
    - Se houver registro de saldo até a data, retorna o último valor.
    - Se não houver nenhum movimento anterior, retorna 0.
    """
    try:
        conexao.execute("""
            SELECT valor 
            FROM saldo
            WHERE DATE(DATA) <= DATE(?)
            ORDER BY DATA DESC, id_saldo DESC
            LIMIT 1;
        """, (data,))
        resultado = conexao.fetchone()
        if resultado:
            return float(resultado[0])
        else:
            return 0.0
    except Exception as e:
        print(f"Erro ao buscar saldo por data: {e}")
        return None
def mostrar_movimentos(conexao=cursor):
    conexao.execute("SELECT * FROM movimento_financeiro ORDER BY id_movimento DESC;")
    movimentos_banco=conexao.fetchall()
    movimentos={}
    print(movimentos_banco)
    for movimento in movimentos_banco:
        tipo_movimento='Entrada'
        
        if (movimento[3] == 0 ):
            tipo_movimento='Saída'
        movimentos[movimento[0]]={
                'data':movimento[1],
                'movimento':tipo_movimento,
                'tipo_movimento':movimento[4],
                'valor':movimento[5],
                'obs':movimento[6]
            }
    return movimentos
def mostrar_movimentos_periodo(inicio,fim,conexao=cursor):
    conexao.execute("SELECT * FROM movimento_financeiro WHERE data BETWEEN ? AND ? ORDER BY id_movimento DESC;",(inicio,fim))
    movimentos_banco=conexao.fetchall()
    movimentos={}
    for movimento in movimentos_banco:
        tipo_movimento='Entrada'
        if (movimento[3] == 0 ):
            tipo_movimento='Saída'
        movimentos[movimento[0]]={
                'data':movimento[1],
                'movimento':tipo_movimento,
                'tipo_movimento':movimento[4],
                'valor':movimento[5],
                'obs':movimento[6]
            }
    return movimentos
def mostrar_membros_all(conexao=cursor, estado=str):
    if estado == 'Professo':
        conexao.execute("SELECT * FROM PROFESSOS;")
        lista_professos_banco = conexao.fetchall()
        lista_professos = {}

        for professo in lista_professos_banco:
            ativo = 'sim' if professo[10] == 1 else 'não'
            lista_professos[professo[0]] = {
                'id_professo': professo[0],
                'nome': professo[1],
                'endereco': professo[2],
                'data_ppfb': professo[3],
                'data_nasc': professo[4],
                'identidade': professo[5],
                'cpf': professo[6],
                'telefone': professo[7],
                'forma_admissao': professo[8],
                'genero': professo[9],
                'ativo': ativo
            }
        return lista_professos

    elif estado == 'Menores':
        conexao.execute("SELECT * FROM MENORES;")
        lista_menores_banco = conexao.fetchall()
        lista_menores = {}
        for menor in lista_menores_banco:
            ativo = 'sim' if menor[7] == 1 else 'não'
            lista_menores[menor[0]] = {
                'id_menor': menor[0],
                'nome': menor[1],
                'nome_pai': menor[2],
                'nome_mae': menor[3],
                'responsavel': menor[4],
                'telefone': menor[5],
                'data_nasc': menor[6],
                'ativo': ativo
            }
        return lista_menores

    elif estado == 'Agregados':
        conexao.execute("SELECT * FROM AGREGADOS;")
        lista_agregados_banco = conexao.fetchall()
        lista_agregados = {}
        for agregado in lista_agregados_banco:
            ativo = 'sim' if agregado[4] == 1 else 'não'
            lista_agregados[agregado[0]] = {
                'id_agregado': agregado[0],
                'nome': agregado[1],
                'telefone': agregado[2],
                'endereco': agregado[3],
                'ativo': ativo
            }
        return lista_agregados

    else:
        print(f"estado {estado} não encontrado")
        return {}
def buscar_professo_por_nome(nome, conexao=cursor):
    """
    Busca um professo pelo nome no banco de dados.
    Retorna um dicionário com os dados ou None se não encontrar.
    """
    conexao.execute("SELECT * FROM PROFESSOS WHERE NOME = ?;", (nome,))
    professo = conexao.fetchone()

    if professo:
        return {
            'id_professo': professo[0],
            'nome': professo[1],
            'endereco': professo[2],
            'data_ppfb': professo[3],
            'data_nasc': professo[4],
            'identidade': professo[5],
            'cpf': professo[6],
            'telefone': professo[7],
            'forma_admissao': professo[8],
            'genero': professo[9],
            'ativo': 'sim' if professo[10] == 1 else 'não'
        }
    else:
        return None
def buscar_nome_menor(nome,conexao=cursor):
    nome=str(nome)
    conexao.execute("SELECT * FROM MENORES WHERE NOME=? ;",(nome,))
    menor=conexao.fetchone()
    dados_menor={}
    if menor is None:
        return dados_menor
    else:
        ativo='sim'
        if (menor[7] != 1 ):
           ativo='não'
        dados_menor={
                'id_menor':menor[0],
                'nome':menor[1],
                'nome_pai':menor[2],
                'nome_mae':menor[3],
                'responsavel':menor[4],
                'telefone_responsavel':menor[5],
                'data_nascimento':menor[6],
                'ativo':ativo
            }
        return dados_menor
def buscar_nome_agregado(nome, conexao=cursor):
    nome = str(nome)
    conexao.execute("SELECT * FROM AGREGADOS WHERE NOME = ?;", (nome,))
    agregado = conexao.fetchone()
    dados_agregado = {}

    if agregado is None:
        return False
    else:
        ativo = 'sim' if agregado[4] == 1 else 'não'
        dados_agregado = {
            'id_agregado': agregado[0],
            'nome': agregado[1],
            'telefone': agregado[2],
            'endereco': agregado[3],
            'ativo': ativo
        }
        return dados_agregado
def editar_professos(id_professo, nome, endereco, data_ppfb, data_nasc, identidade, cpf, telefone, forma_admissao, genero, ativo, conexao=cursor):
    try:
        conexao.execute("""
            UPDATE PROFESSOS
            SET NOME = ?, ENDERECO = ?, DATA_PPFB = ?, DATA_NASC = ?, IDENTIDADE = ?, CPF = ?, TELEFONE = ?, FORMA_ADMISSAO = ?, GENERO = ?, ATIVO = ?
            WHERE ID_PROFESSO = ?
        """, (nome, endereco, data_ppfb, data_nasc, identidade, cpf, telefone, forma_admissao, genero, ativo, id_professo))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao editar professo: {e}")
        return False
def desativar_ativar(id, ativo, conexao=cursor, estado=str):
    try:
        if estado == 'Professo':
            conexao.execute("""
                UPDATE PROFESSOS
                SET ATIVO = ?
                WHERE ID_PROFESSO = ?
            """, (ativo, id))
            conn.commit()

            # Registro no histórico
            conexao.execute("""
                INSERT INTO PROFESSOS_DESATIVADOS_ATIVADOS (ID_PROFESSO, ATIVO)
                VALUES (?, ?)
            """, (id, ativo))
            conn.commit()

        elif estado == 'Menores':
            conexao.execute("""
                UPDATE MENORES
                SET ATIVO = ?
                WHERE ID_MENOR = ?
            """, (ativo, id))
            conn.commit()

            # Registro no histórico
            conexao.execute("""
                INSERT INTO MENORES_DESATIVADOS_ATIVADOS (ID_MENOR, ATIVO)
                VALUES (?, ?)
            """, (id, ativo))
            conn.commit()

        elif estado == 'Agregados':
            conexao.execute("""
                UPDATE AGREGADOS
                SET ATIVO = ?
                WHERE ID_AGREGADO = ?
            """, (ativo, id))
            conn.commit()

            # Registro no histórico
            conexao.execute("""
                INSERT INTO AGREGADOS_DESATIVADOS_ATIVADOS (ID_AGREGADO, ATIVO)
                VALUES (?, ?)
            """, (id, ativo))
            conn.commit()

        else:
            print(' Estado não encontrado:', estado)
            return False

        return True

    except Exception as e:
        print(f" Erro ao ativar/desativar {estado}: {e}")
        return False
def buscar_desativado(id, conexao=cursor, estado=str):
    try:
        if estado == "Professo":
            conexao.execute("""
                SELECT * FROM PROFESSOS_DESATIVADOS_ATIVADOS
                WHERE ID_PROFESSO = ?
            """, (id,))
            resultado = conexao.fetchall()

        elif estado == "Menores":
            conexao.execute("""
                SELECT * FROM MENORES_DESATIVADOS_ATIVADOS
                WHERE ID_MENOR = ?
            """, (id,))
            resultado = conexao.fetchall()

        elif estado == "Agregados":
            conexao.execute("""
                SELECT * FROM AGREGADOS_DESATIVADOS_ATIVADOS
                WHERE ID_AGREGADO = ?
            """, (id,))
            resultado = conexao.fetchall()

        else:
            print(" Estado não encontrado:", estado)
            return None

        return resultado if resultado else None

    except Exception as e:
        print(f" Erro ao buscar desativado {estado}: {e}")
        return None
def editar_menores(conexao=cursor,id_menores=int,nome=str,nome_pai=str,nome_mãe=str,responsavel=str,telefone_responsavel=str,data_nasc=str,ativo=bool):
    try:
        conexao.execute("""
            UPDATE MENORES
            SET NOME = ?, NOME_PAI = ?, NOME_MAE = ?, RESPONSAVEL= ?, TELEFONE_RESPONSAVEL = ?, DATA_NASC = ?, ATIVO=?
            WHERE ID_MENOR = ?
        """, (nome,nome_pai,nome_mãe,responsavel,telefone_responsavel,data_nasc,ativo,id_menores))
        conn.commit()
        return True
    except:
        return False
def editar_agregado(id_agregado, nome, telefone, endereco, ativo, conexao=cursor):
    try:
        conexao.execute("""
            UPDATE AGREGADOS
            SET NOME = ?, TELEFONE = ?, ENDERECO = ?, ATIVO = ?
            WHERE ID_AGREGADO = ?
        """, (nome, telefone, endereco, ativo, id_agregado))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao editar agregado: {e}")
        return False
def buscar_professo_transferido(id_professo, conexao=cursor):
    """
    Busca os dados de transferência de um professo pelo ID.
    Retorna dicionário com igreja, data e caminho do arquivo salvo.
    """
    try:
        conexao.execute("""
            SELECT IGREJA_ORIGEM, DATA_TRASNF, CARTA
            FROM PROFESSOS_TRANSFERIDOS
            WHERE ID_PROFESSO_TRANSFERIDO = ?;
        """, (id_professo,))
        resultado = conexao.fetchone()

        if resultado is None:
            return None  # não existe transferência cadastrada

        igreja_origem, data_transf, carta_blob = resultado

        # Se tiver arquivo, salvar em arquivo temporário
        caminho_arquivo = None
        if carta_blob:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(carta_blob)
                caminho_arquivo = tmp.name

        return {
            "igreja_origem": igreja_origem,
            "data_transferencia": data_transf,
            
        }

    except Exception as e:
        print(f"Erro ao buscar transferência: {e}")
        return None

def baixar_arquivo_transferencia(self, id_professo, conexao=cursor):
    """
    Permite o usuário baixar o PDF da transferência para uma pasta escolhida.
    """
    try:
        conexao.execute("""
            SELECT CARTA FROM PROFESSOS_TRANSFERIDOS
            WHERE ID_PROFESSO_TRANSFERIDO = ?;
        """, (id_professo,))
        resultado = conexao.fetchone()

        if resultado is None or resultado[0] is None:
            QMessageBox.warning(self, "Aviso", "Nenhum arquivo encontrado para este professo.")
            return

        carta_blob = resultado[0]

        # Abrir janela para escolher onde salvar
        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar arquivo",
            "carta_transferencia.pdf",
            "Arquivos PDF (*.pdf)"
        )

        if caminho:  # Se o usuário escolheu um caminho
            with open(caminho, "wb") as f:
                f.write(carta_blob)
            QMessageBox.information(self, "Sucesso", f"Arquivo salvo em:\n{caminho}")

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Erro ao baixar arquivo:\n{e}")
def salvar_dados_professo(self, dados):
    """Salva os dados do formulário no banco de dados."""
    try:
        from conect_banco import conn  # use sua conexão
        cursor = conn.cursor()

        # Atualiza tabela PROFESSOS
        cursor.execute("""
            UPDATE PROFESSOS
            SET
                NOME = ?,
                ENDERECO = ?,
                IDENTIDADE = ?,
                CPF = ?,
                TELEFONE = ?,
                DATA_NASC = ?,
                DATA_PPFB = ?,
                GENERO = ?,
                FORMA_ADMISSAO = ?,
                ATIVO = ?
            WHERE ID_PROFESSO = ?;
        """, (
            dados['nome'],
            dados['endereco'],
            dados['identidade'],
            dados['cpf'],
            dados['telefone'],
            dados['data_nasc'],
            dados['data_ppfb'],
            dados['genero'],
            dados['forma_admissao'],
            dados['ativo'],
            dados['id_professo']
        ))

        # Se houver carta de transferência, atualiza PROFESSOS_TRANSFERIDOS
        if dados['forma_admissao'] == "Carta de Transferencia":
            cursor.execute("""
                UPDATE PROFESSOS_TRANSFERIDOS
                SET
                    IGREJA_ORIGEM = ?,
                    DATA_TRASNF = ?
                WHERE ID_PROFESSO_TRANSFERIDO = ?;
            """, (
                dados['igreja_transferida'],
                dados['data_transferencia'],
                dados['id_professo']
            ))

        conn.commit()
        QMessageBox.information(self, "Sucesso", "Dados salvos com sucesso!")
    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Erro ao salvar dados:\n{e}")
#Junta diagonal 
def mostrar_junta_diagonal(conexao=cursor):
    """
    Retorna todos os membros da Junta Diaconal
    com os dados completos dos professos relacionados.
    A data de saída é sempre 1 ano após a data de entrada.
    """
    try:
        conexao.execute("""
            SELECT jd.ID_JUNTA, jd.DATA_ENTRADA, p.*
            FROM JUNTA_DIAGONAL jd
            JOIN PROFESSOS p ON jd.ID_PROFESSO = p.ID_PROFESSO;
        """)
        resultados = conexao.fetchall()

        lista = {}
        for row in resultados:
            id_junta = row[0]
            data_entrada = row[1]

            # Converter para datetime
            try:
                data_entrada_dt = datetime.strptime(data_entrada, "%Y-%m-%d %H:%M:%S")
            except:
                data_entrada_dt = datetime.strptime(data_entrada, "%Y-%m-%d")

            # Data de saída = 1 ano depois
            data_saida_dt = data_entrada_dt + timedelta(days=365)
            data_saida = data_saida_dt.strftime("%Y-%m-%d")

            id_professo = row[2]
            lista[id_junta] = {
                'id_junta': id_junta,
                'id_professo': id_professo,
                'nome': row[3],
                'endereco': row[4],
                'data_ppfb': row[5],
                'data_nasc': row[6],
                'identidade': row[7],
                'cpf': row[8],
                'telefone': row[9],
                'forma_admissao': row[10],
                'genero': row[11],
                'ativo': 'sim' if row[12] == 1 else 'não',
                'data_entrada': data_entrada,
                'data_saida': data_saida
            }
        return lista

    except Exception as e:
        print(f" Erro ao buscar Junta Diaconal: {e}")
        return {}
def adicionar_professo_na_junta(id_professo,nome ,conexao=cursor):
    """
    Adiciona um professo à Junta Diaconal.
    """
    try:
        conexao.execute("""
            INSERT INTO JUNTA_DIAGONAL (ID_PROFESSO,NOME)
            VALUES (?,?);
        """, (id_professo,nome))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao adicionar professo na Junta Diaconal: {e}")
        return False
def remover_professo_da_junta(id_junta, conexao=cursor):
    """
    Remove um membro da Junta Diaconal pelo ID_JUNTA.
    """
    try:
        conexao.execute("""
            DELETE FROM JUNTA_DIAGONAL
            WHERE ID_JUNTA = ?;
        """, (id_junta,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao remover professo da Junta Diaconal: {e}")
        return False
def mostrar_conselho(conexao=cursor):
    """
    Retorna todos os membros do Conselho
    com os dados completos dos professos relacionados.
    A data de saída é sempre 1 ano após a data de entrada.
    """
    try:
        conexao.execute("""
            SELECT c.ID_CONSELHO, c.DATA_ENTRADA, p.*
            FROM CONSELHO c
            JOIN PROFESSOS p ON c.ID_PROFESSO = p.ID_PROFESSO;
        """)
        resultados = conexao.fetchall()

        lista = {}
        for row in resultados:
            id_conselho = row[0]
            data_entrada = row[1]

            # Converter para datetime
            try:
                data_entrada_dt = datetime.strptime(data_entrada, "%Y-%m-%d %H:%M:%S")
            except:
                data_entrada_dt = datetime.strptime(data_entrada, "%Y-%m-%d")

            # Data de saída = 1 ano depois
            data_saida_dt = data_entrada_dt + timedelta(days=365)
            data_saida = data_saida_dt.strftime("%Y-%m-%d")

            id_professo = row[2]
            lista[id_conselho] = {
                'id_conselho': id_conselho,
                'id_professo': id_professo,
                'nome': row[3],
                'endereco': row[4],
                'data_ppfb': row[5],
                'data_nasc': row[6],
                'identidade': row[7],
                'cpf': row[8],
                'telefone': row[9],
                'forma_admissao': row[10],
                'genero': row[11],
                'ativo': 'sim' if row[12] == 1 else 'não',
                'data_entrada': data_entrada,
                'data_saida': data_saida
            }
        return lista

    except Exception as e:
        print(f" Erro ao buscar Conselho: {e}")
        return {}
def adicionar_professo_no_conselho(id_professo, conexao=cursor):
    """
    Adiciona um professo ao Conselho.
    """
    try:
        conexao.execute("""
            INSERT INTO CONSELHO (ID_PROFESSO)
            VALUES (?);
        """, (id_professo,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao adicionar professo no Conselho: {e}")
        return False
def remover_professo_do_conselho(id_conselho, conexao=cursor):
    """
    Remove um membro do Conselho pelo ID_CONSELHO.
    """
    try:
        conexao.execute("""
            DELETE FROM CONSELHO
            WHERE ID_CONSELHO = ?;
        """, (id_conselho,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao remover professo do Conselho: {e}")
        return False
 #-----------------------------------
 #Gestão de funçoes 
 # =============================
# FUNÇÕES DE CADASTRO DE MINISTÉRIOS
# =============================

#Para a tabela FUNCOES vai funcionar da seguinte forma :
#id do membro
#nome do membro
#para area do membro podendo ser  louvor,eventos_especias,cozinha,escola_domical,ministerio_oracao,dep_infatil
#função do membro podendo ser quaquer uma que ele colocar
#data de entrada do membro na função
# ================================
#      CRUD - TABELA FUNCOES
# ================================

def cadastrar_funcao(id_membro, nome, area, funcao, data_entrada, conexao=cursor):
    """Cadastra uma nova função para um membro."""
    try:
        conexao.execute("""
            INSERT INTO FUNCOES (ID_MEMBRO, NOME, AREA, FUNCAO, DATA_ENTRADA)
            VALUES (?, ?, ?, ?, ?)
        """, (id_membro, nome, area, funcao, data_entrada))
        conn.commit()
        print(f" Função '{funcao}' cadastrada com sucesso para {nome}.")
        return True
    except Exception as e:
        print(f" Erro ao cadastrar função: {e}")
        return False
def listar_funcoes(conexao=cursor):
    """Retorna todas as funções cadastradas."""
    try:
        conexao.execute("SELECT * FROM FUNCOES ORDER BY ID DESC")
        registros = conexao.fetchall()
        funcoes = {}

        for row in registros:
            funcoes[row[0]] = {
                'id': row[0],
                'id_membro': row[1],
                'nome': row[2],
                'area': row[3],
                'funcao': row[4],
                'data_entrada': row[5]
            }
        return funcoes
    except Exception as e:
        print(f" Erro ao listar funções: {e}")
        return {}
def buscar_funcao_por_nome(nome, conexao=cursor):
    """Busca todas as funções associadas a um nome."""
    try:
        conexao.execute("SELECT * FROM FUNCOES WHERE NOME LIKE ?", (f"%{nome}%",))
        registros = conexao.fetchall()

        if not registros:
            return None

        resultados = []
        for row in registros:
            resultados.append({
                'id': row[0],
                'id_membro': row[1],
                'nome': row[2],
                'area': row[3],
                'funcao': row[4],
                'data_entrada': row[5]
            })
        return resultados
    except Exception as e:
        print(f" Erro ao buscar função por nome: {e}")
        return None
def editar_funcao(id_funcao, id_membro, nome, area, funcao, data_entrada, conexao=cursor):
    """Edita uma função existente."""
    try:
        conexao.execute("""
            UPDATE FUNCOES
            SET ID_MEMBRO = ?, NOME = ?, AREA = ?, FUNCAO = ?, DATA_ENTRADA = ?
            WHERE ID = ?
        """, (id_membro, nome, area, funcao, data_entrada, id_funcao))
        conn.commit()
        print(f" Função ID {id_funcao} atualizada com sucesso.")
        return True
    except Exception as e:
        print(f" Erro ao editar função: {e}")
        return False
def deletar_funcao(id_funcao, conexao=cursor):
    """Exclui uma função do banco de dados."""
    try:
        conexao.execute("DELETE FROM FUNCOES WHERE ID = ?", (id_funcao,))
        conn.commit()
        print(f" Função ID {id_funcao} deletada com sucesso.")
        return True
    except Exception as e:
        print(f" Erro ao deletar função: {e}")
        return False
def buscar_funcoes_por_area(area, conexao=cursor):
    """
    Retorna todas as funções cadastradas em uma área específica.
    Exemplo: buscar_funcoes_por_area("LOUVOR")
    """
    try:
        conexao.execute("""
            SELECT ID, ID_MEMBRO, NOME, AREA, FUNCAO, DATA_ENTRADA
            FROM FUNCOES
            WHERE AREA = ?
            ORDER BY NOME ASC
        """, (area,))
        registros = conexao.fetchall()

        if not registros:
            print(f" Nenhum registro encontrado para a área '{area}'.")
            return {}

        funcoes = {}
        for row in registros:
            funcoes[row[1]]={
                'id': row[0],
                'id_membro': row[1],
                'nome': row[2],
                'area': row[3],
                'funcao': row[4],
                'data_entrada': row[5]
            }
        return funcoes

    except Exception as e:
        print(f" Erro ao buscar funções por área: {e}")
        return {}
#CADASTRO,EDIÇÃO E ATIVAÇÃO OU DESATIVAÇÃO DE MEMBROS
#Cadastrar Membro
def  cadastrar_professo(nome, endereco, data_ppfb, data_nasc, identidade, cpf, telefone, forma_admissao, genero, conexao=cursor):
    try:
        conexao.execute("""
            INSERT INTO PROFESSOS (NOME, ENDERECO, DATA_PPFB, DATA_NASC, IDENTIDADE, CPF, TELEFONE, FORMA_ADMISSAO, GENERO, ATIVO)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, TRUE)
        """, (nome, endereco, data_ppfb, data_nasc, identidade, cpf, telefone, forma_admissao, genero))
        conn.commit()
        conexao.execute("SELECT ID_PROFESSO FROM PROFESSOS ORDER BY ID_PROFESSO DESC LIMIT 1")
        id=conexao.fetchone()[0]
        cursor.execute("INSERT INTO PROFESSOS_DESATIVADOS_ATIVADOS(ID_PROFESSO,ATIVO) VALUES(?,TRUE)",(id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar professo: {e}")
        return False
def cadastrar_professo_transferido(id_professo, igreja_transferida, data_transferencia, carta,conexao=cursor):
    try:
        
        conexao.execute("""
            INSERT INTO PROFESSOS_TRANSFERIDOS 
            (ID_PROFESSO_TRANSFERIDO, IGREJA_ORIGEM, DATA_TRASNF,CARTA)
            VALUES (?, ?, ? , ?);
        """, (id_professo, igreja_transferida, data_transferencia,carta))
        conn.commit()
        
        return True
    except sqlite3.Error as e:
        print("Erro ao inserir professo transferido:", e)
        return False
def cadastrar_menores(nome,nome_pai,nome_mãe,responsavel,telefone_responsavel,data_nasc,conexao=cursor):
    try:
        conexao.execute("""
            INSERT INTO MENORES (NOME, NOME_PAI, NOME_MAE, RESPONSAVEL, TELEFONE_RESPONSAVEL , DATA_NASC,ATIVO)
            VALUES (?, ?, ?, ?, ?,?,TRUE)
        """, (nome,nome_pai,nome_mãe,responsavel,telefone_responsavel,data_nasc))
        conn.commit()
        conexao.execute("SELECT ID_MENOR FROM MENORES ORDER BY ID_MENOR DESC LIMIT 1")
        id=conexao.fetchone()[0]
        cursor.execute("INSERT INTO MENORES_DESATIVADOS_ATIVADOS(ID_MENOR,ATIVO) VALUES(?,TRUE)",(id,))
        conn.commit()
        return True
    except Exception as e:
         print(f"O tipo de erro é : {type(e).__name__}")
         print(f"Mensageem de erro e {e}")
         return False
def cadastrar_agregados(nome,telefone,endereco,conexao=cursor):
    try:
        conexao.execute("""
            INSERT INTO AGREGADOS (NOME, TELEFONE, ENDERECO,ATIVO)
            VALUES (?, ?, ?,TRUE)
        """, (nome,telefone,endereco))
        conn.commit()
        conexao.execute("SELECT ID_AGREGADO FROM AGREGADOS ORDER BY ID_AGREGADO DESC LIMIT 1")
        id=conexao.fetchone()[0]
        cursor.execute("INSERT INTO AGREGADOS_DESATIVADOS_ATIVADOS(ID_AGREGADO,ATIVO) VALUES(?,TRUE)",(id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar professo: {e}")
        return False
# ================= USUÁRIOS E PERMISSÕES ==================

def cadastrar_usuario(nome, senha, tipo_usuario, nome_criador,id_criador, ativo,permisoes,conexao=cursor,conn=conn):
    """
    Cadastra um novo usuário no sistema.
    """
    try:
        conexao.execute("""
            INSERT INTO USUARIOS (NOME, SENHA,tipo_usuario,ID_CRIADOR,NOME_CRIADOR,ATIVO)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, senha, tipo_usuario,id_criador, nome_criador,ativo))
        conn.commit()
        conexao.execute("SELECT * FROM USUARIOS ORDER BY ID DESC LIMIT 1")
        retorno=conexao.fetchone()
        id_retorno=retorno[0]
        nome_retorno=retorno[1]
        tipo_usuario_retorno=retorno[3]
        id_usaurio_criador=retorno[5]
        nome_usuario_criador=retorno[6]
        retorno_p=definir_permissoes(id_usuario=id_retorno,nome_usuario=nome_retorno,id_permissor=id_usaurio_criador,nome_permissor=nome_usuario_criador,financa=permisoes['financas'], gestao_membros=permisoes['cadastro_membros'], gestao_funcoes=permisoes['gestao_funcoes'], gestao_usuarios=permisoes['gestao_usuarios'])
        print("retorno_p:",retorno_p)
        if retorno_p: print("Permissoes salvas com sucesso")
        
        return True
    except Exception as e:
        print(f" Erro ao cadastrar usuário: {e}")
        return False
def autenticar_usuario(nome, senha, conexao=cursor):
    """
    Verifica se o usuário e senha são válidos.
    Retorna um dicionário com os dados se for válido, ou None se não existir.
    """
    try:
        conexao.execute("""
            SELECT * FROM USUARIOS WHERE NOME = ? AND SENHA = ? AND ATIVO = 1;
        """, (nome, senha))
        usuario = conexao.fetchone()

        if usuario:
            return (True,usuario)
        else:
            return (False,usuario)
    except Exception as e:
        print(f" Erro ao autenticar usuário: {e}")
        return None
def editar_usuario(id_usuario, nome, tipo_usuario, ativo, conexao=cursor):
    """
    Edita os dados de um usuário.
    """
    try:
        conexao.execute("""
            UPDATE USUARIOS
            SET NOME = ?, tipo_usuario = ?, ATIVO = ?
            WHERE ID = ?;
        """, (nome, tipo_usuario, ativo, id_usuario))
        conn.commit()
        print(f" Usuário ID {id_usuario} atualizado.")
        return True
    except Exception as e:
        print(f" Erro ao editar usuário: {e}")
        return False
def desativar_ativar_usuario(id_usuario,nome_usuario, ativo, conexao=cursor):
    """
    Ativa ou desativa um usuário.
    """
    try:
        conexao.execute("""
            UPDATE USUARIOS SET ATIVO = ? WHERE ID = ? AND NOME=?;
        """, (ativo, id_usuario,nome_usuario))
        conn.commit()
        print(f" Usuário {id_usuario} {'ativado' if ativo else 'desativado'}.")
        return True
    except Exception as e:
        print(f" Erro ao ativar/desativar usuário: {e}")
        return False
def mostrar_usuarios(conexao=cursor):
    """
    Retorna todos os usuários cadastrados.
    """
    conexao.execute("SELECT * FROM USUARIOS ORDER BY ID DESC;")
    usuarios_banco = conexao.fetchall()
    usuarios = {}
    for usuario in usuarios_banco:
        ativo = 'sim' if usuario[7] == 1 else 'não'
        usuarios[usuario[0]] = {
            'id': usuario[0],
            'nome': usuario[1],
            'senha':usuario[2],
            'tipo_usuario': usuario[3],
            'data_entrada': usuario[4],
            'ativo': ativo
        }
    return usuarios
def alterar_senha_usuario(id_usuario,nome_usuario, senha_atual, nova_senha):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verifica se o usuário existe e se a senha atual está correta
        cursor.execute("SELECT SENHA FROM USUARIOS WHERE ID = ? AND NOME=?", (id_usuario,nome_usuario,))
        resultado = cursor.fetchone()

        if not resultado:
            print(" Usuário não encontrado.")
            return False
        
        senha_banco = resultado[0]
        if senha_banco != senha_atual:
            print(" Senha atual incorreta.")
            return False

        # Atualiza a senha
        cursor.execute(
            "UPDATE USUARIOS SET SENHA = ? WHERE NOME = ?",
            (nova_senha, nome_usuario)
        )

        conn.commit()
        conn.close()
        print(" Senha alterada com sucesso!")
        return True

    except Exception as e:
        print(f" Erro ao alterar senha: {e}")
        return False
# ---------------------- PERMISSÕES ----------------------

def definir_permissoes(id_usuario, nome_usuario,id_permissor, nome_permissor,
                       financa, gestao_membros, gestao_funcoes, gestao_usuarios, conexao=cursor,conn=conn):
    """
    Define ou atualiza permissões para um usuário.
    """
    try:
        conexao.execute("""
            SELECT ID FROM PERMISSOES WHERE ID_USUARIO = ?;
        """, (id_usuario,))
        existe = conexao.fetchone()
        print('existe:',existe)
        if existe :
            conexao.execute("""
                UPDATE PERMISSOES
                SET FINANCA = ?, GESTAO_MEMBROS = ?, GESTAO_FUNCOES = ?, GESTAO_USUARIOS = ?
                WHERE ID_USUARIO = ?;
            """, (financa, gestao_membros, gestao_funcoes, gestao_usuarios, id_usuario))

        else:
            conexao.execute("""
                INSERT INTO PERMISSOES 
                (ID_USUARIO, NOME_USUARIO,  ID_USUARIO_P, NOME_USUARIO_P,
                 FINANCA, GESTAO_MEMBROS, GESTAO_FUNCOES, GESTAO_USUARIOS)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (id_usuario, nome_usuario, id_permissor, nome_permissor,
                  financa, gestao_membros, gestao_funcoes, gestao_usuarios))
        conn.commit()
        print(f" Permissões definidas para usuário {nome_usuario}.")
        return True
    except Exception as e:
        print(f" Erro ao definir permissões: {e}")
        return False
def buscar_permissoes(id_usuario, conexao=cursor):
    """
    Retorna as permissões de um usuário específico.
    """
    try:
        conexao.execute("""
            SELECT FINANCA, GESTAO_MEMBROS, GESTAO_FUNCOES, GESTAO_USUARIOS
            FROM PERMISSOES
            WHERE ID_USUARIO = ?;
        """, (id_usuario,))
        resultado = conexao.fetchone()

        if resultado:
            return {
                'financa': bool(resultado[0]),
                'gestao_membros': bool(resultado[1]),
                'gestao_funcoes': bool(resultado[2]),
                'gestao_usuarios': bool(resultado[3])
            }
        else:
            return {
                'financa': False,
                'gestao_membros': False,
                'gestao_funcoes': False,
                'gestao_usuarios': False
            }
    except Exception as e:
        print(f" Erro ao buscar permissões: {e}")
        return None
def listar_permissoes(conexao=cursor):
    """
    Lista todas as permissões cadastradas no sistema.
    """
    try:
        conexao.execute("""
            SELECT * FROM PERMISSOES ORDER BY ID DESC;
        """)
        permissoes_banco = conexao.fetchall()
        permissoes = {}
        for p in permissoes_banco:
            permissoes[p[0]] = {
                'id_usuario': p[1],
                'nome_usuario': p[2],
                'tipo_usuario': p[3],
                'autorizado_por': p[5],
                'financa': 'sim' if p[7] else 'não',
                'gestao_membros': 'sim' if p[8] else 'não',
                'gestao_funcoes': 'sim' if p[9] else 'não',
                'gestao_usuarios': 'sim' if p[10] else 'não'
            }
        return permissoes
    except Exception as e:
        print(f" Erro ao listar permissões: {e}")
        return {}
# ======================================
# CRUD - VERSÍCULOS
# ======================================

def cadastrar_vesiculo( livro, versiculo, conexao=cursor):
    """
    Cadastra um novo versículo no banco.
    """
    try:
        conexao.execute("""
            INSERT INTO VESICULOS (LIVRO, VERSICULO)
            VALUES (?, ?)
        """, ( livro, versiculo))
        conn.commit()
        print(" Versículo cadastrado com sucesso.")
        conexao.execute("""
            SELECT ID, LIVRO, VERSICULO, DATA_CADASTRO
            FROM VESICULOS
            ORDER BY ID DESC
        """)
        id_inserido = cursor.lastrowid

        print(f" Versículo cadastrado com sucesso (ID: {id_inserido})")
        return id_inserido  # retorna o ID do versículo cadastrado
    except Exception as e:
        print(f" Erro ao cadastrar versículo: {e}")     
def listar_vesiculos(conexao=cursor):
    """
    Retorna todos os versículos cadastrados no sistema.
    """
    try:
        conexao.execute("""
            SELECT ID, LIVRO, VERSICULO, DATA_CADASTRO
            FROM VESICULOS
            ORDER BY ID DESC
        """)
        resultado = conexao.fetchall()
        lista = []
        for v in resultado:
            lista.append({
                "id": v[0],
                "livro": v[1],
                "versiculo": v[2],
                "data_cadastro": v[3]
            })
        return lista
    except Exception as e:
        print(f" Erro ao listar versículos: {e}")
        return []
def buscar_vesiculo_por_id(id_vesiculo, conexao=cursor):
    """
    Busca um versículo pelo ID.
    """
    try:
        conexao.execute("""
            SELECT ID, LIVRO, VERSICULO, DATA_CADASTRO
            FROM VESICULOS
            WHERE ID = ? ;
        """, (id_vesiculo,))
        resultado = conexao.fetchone()
        if resultado:
            return {
                "id": resultado[0],
                "livro": resultado[1],
                "versiculo": resultado[2],
                "data_cadastro": resultado[3]
            }
        return None
    except Exception as e:
        print(f" Erro ao buscar versículo: {e}")
        return None
def editar_vesiculo(id_vesiculo, novo_livro, novo_versiculo, conexao=cursor):
    """
    Edita o texto ou o livro de um versículo.
    """
    try:
        conexao.execute("""
            UPDATE VESICULOS
            SET LIVRO = ?, VERSICULO = ?
            WHERE ID = ?
        """, (novo_livro, novo_versiculo, id_vesiculo))
        conn.commit()
        print(f" Versículo ID {id_vesiculo} atualizado com sucesso.")
        return True
    except Exception as e:
        print(f" Erro ao editar versículo: {e}")
        return False
def deletar_vesiculo(id_vesiculo, conexao=cursor):
    """
    Remove um versículo do banco.
    """
    try:
        conexao.execute("""
            DELETE FROM VESICULOS WHERE ID = ?
        """, (id_vesiculo,))
        conn.commit()
        print(f" Versículo ID {id_vesiculo} removido com sucesso.")
        return True
    except Exception as e:
        print(f" Erro ao deletar versículo: {e}")
        return False
def buscar_versiculo_atual(conexao=conn):
    """
    Retorna o versículo correspondente à data atual (entre DATA_EXPOSICAO_INICIAL e DATA_EXPOSICAO_FINAL).
    """
    try:
        cursor = conexao.cursor()
        data_hoje = datetime.now().date()

        cursor.execute("""
            SELECT * FROM VESICULO_atual  ORDER BY ID DESC
            LIMIT 1;
           
        """, ())

        resultado = cursor.fetchone()
        if resultado:
          return resultado
        else:
            return ()
    except Exception as e:
        print(f" Erro ao buscar versículo atual: {e}")
        return None
def inserir_versiculo_atual(livro, versiculo,  conexao=conn):
    """
    Insere um novo versículo na tabela VESICULO_atual com data inicial e final de exibição.
    """
    try:
        cursor = conexao.cursor()
       
        cursor.execute("""
            INSERT INTO VESICULO_atual (LIVRO, VERSICULO)
            VALUES (?, ?)
        """, (livro, versiculo))
        conexao.commit()

        # Retorna o ID recém inserido
        cursor.execute("SELECT last_insert_rowid()")
        id_inserido = cursor.fetchone()[0]

        print(f" Versículo inserido com sucesso! (ID: {id_inserido})")
        return id_inserido

    except Exception as e:
        print(f" Erro ao inserir versículo atual: {e}")
        return None
#----------------------------
print(mostrar_conselho())