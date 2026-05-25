import sqlite3
from src.models.usuario import Usuario

class SqliteRepository:
    
    def __init__(self, db_nome="easyfinance.db"):
        self.db_nome = db_nome
        self._criar_tabelas()

    def _conectar(self):
        """Abre a conexão com o banco SQlite"""
        conn = sqlite3.connect(self.db_nome)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _criar_tabelas(self):
        """Cria as tabelas no banco de dados caso elas não existam"""
        with self._conectar() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios(
                    email TEXT PRIMARY KEY,
                    documento TEXT,
                    senha TEXT,
                    pontos INTEGER,
                    ranking TEXT          
                           
                 )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_email TEXT,
                    tipo TEXT,
                    descricao TEXT,
                    valor REAL,
                    FOREIGN KEY (usuario_email) REFERENCES usuarios (email)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_email TEXT,
                    objetivo TEXT,
                    valor REAL,
                    FOREIGN KEY (usuario_email) REFERENCES usuarios (email)
                )
            ''')
            
            # Tabela de Lembretes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lembretes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_email TEXT,
                    conta TEXT,
                    data TEXT,
                    FOREIGN KEY (usuario_email) REFERENCES usuarios (email)
                )
            ''')
            conn.commit()

    def email_existe(self, email: str) -> bool:
        """Verifica se o email já está no banco de dados."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM usuarios WHERE email = ?', (email,))
            return cursor.fetchone() is not None
        
    def buscar_usuario_por_email(self, email: str) -> Usuario:
        """Busca o usuário e todas as suas listas aninhadas no banco. """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
            linha_user = cursor.fetchone()

            if not linha_user:
                return None
            
            usuario = Usuario(
                email=linha_user['email'],
                documento=linha_user['documento'],
                senha=linha_user['senha']
            )
            usuario.pontos = linha_user['pontos']
            usuario.ranking = linha_user['ranking']

            cursor.execute('SELECT tipo, descricao, valor FROM transacoes WHERE usuario_email = ?', (email,))
            usuario.transacoes = [{"tipo": r["tipo"], "descricao": r["descricao"], "valor": r["valor"]} for r in cursor.fetchall()]

            cursor.execute('SELECT objetivo, valor FROM metas WHERE usuario_email = ?', (email,))
            usuario.metas = [{"objetivo": r["objetivo"], "valor": r["valor"]}for r in cursor.fetchall()]

            cursor.execute('SELECT conta, data FROM lembretes WHERE usuario_email = ?', (email,))
            usuario.lembretes = [{"conta":r["conta"], "data": r["data"]}for r in cursor.fetchall()]

            return usuario
        
    def salvar_usuario(self, usuario: Usuario):
        """Salva ou atualiza o usuário e suas listas no banco de dados."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (email, documento, senha, pontos, ranking)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    documento=excluded.documento,
                    senha=excluded.senha,
                    pontos=excluded.pontos,
                    ranking=excluded.ranking
            ''', (
                usuario.email, 
                usuario.documento, 
                usuario.senha, 
                getattr(usuario, 'pontos', 0), 
                getattr(usuario, 'ranking', 'Iniciante')
            ))

            # ... o resto continua igualzinho (os deletes e inserts das listas) ...

            cursor.execute('DELETE FROM transacoes WHERE usuario_email = ?', (usuario.email,))
            cursor.execute('DELETE FROM metas WHERE usuario_email = ?', (usuario.email,))
            cursor.execute('DELETE FROM lembretes WHERE usuario_email = ?', (usuario.email,))

            if hasattr(usuario, 'transacoes'):
                for t in usuario.transacoes:
                    cursor.execute('''
                        INSERT INTO transacoes (usuario_email, tipo, descricao, valor)
                        VALUES (?, ?, ?, ?)
                    ''', (usuario.email, t.get('tipo'), t.get('descricao'), t.get('valor')))
            if hasattr(usuario, 'metas'):
                for m in usuario.metas:
                    cursor.execute('''
                        INSERT INTO metas (usuario_email, objetivo, valor)
                        VALUES (?, ?, ?)
                    ''', (usuario.email, m.get('objetivo'), m.get('valor')))
            if hasattr(usuario, 'lembretes'):
                for l in usuario.lembretes:
                    cursor.execute('''
                        INSERT INTO lembretes (usuario_email, conta, data)
                        VALUES (?, ?, ?)
                    ''', (usuario.email, l.get('conta'), l.get('data')))

            conn.commit()
