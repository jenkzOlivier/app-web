import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('rede_social.db')
cursor = conn.cursor()


# Criar tabelas
def criar_tabelas():
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    ''')

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS postagens (
        id INTEGER PRIMARY KEY,
        autor_id INTEGER,
        conteudo TEXT,
        likes INTEGER DEFAULT 0
    )
    ''')

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS comentarios (
        id INTEGER PRIMARY KEY,
        postagem_id INTEGER,
        autor_id INTEGER,
        texto TEXT
    )
    ''')

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS seguidores (
        seguidor_id INTEGER,
        seguido_id INTEGER,
        PRIMARY KEY (seguidor_id, seguido_id)
    )
    ''')

  conn.commit()


# Funções de registro e login
def registrar_usuario(username, password):
  cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)",
                 (username, password))
  conn.commit()


def fazer_login(username, password):
  cursor.execute("SELECT id FROM usuarios WHERE username = ? AND password = ?",
                 (username, password))
  user_id = cursor.fetchone()
  return user_id


# Funções para postagens
def criar_postagem(autor_id, conteudo):
  cursor.execute("INSERT INTO postagens (autor_id, conteudo) VALUES (?, ?)",
                 (autor_id, conteudo))
  conn.commit()


def listar_postagens():
  cursor.execute("SELECT * FROM postagens")
  return cursor.fetchall()


# Funções para comentários
def adicionar_comentario(postagem_id, autor_id, texto):
  cursor.execute(
      "INSERT INTO comentarios (postagem_id, autor_id, texto) VALUES (?, ?, ?)",
      (postagem_id, autor_id, texto))
  conn.commit()


def listar_comentarios(postagem_id):
  cursor.execute("SELECT * FROM comentarios WHERE postagem_id = ?",
                 (postagem_id, ))
  return cursor.fetchall()


# Funções para seguir e deixar de seguir
def seguir_usuario(seguidor_id, seguido_id):
  cursor.execute(
      "INSERT INTO seguidores (seguidor_id, seguido_id) VALUES (?, ?)",
      (seguidor_id, seguido_id))
  conn.commit()


def deixar_de_seguir(seguidor_id, seguido_id):
  cursor.execute(
      "DELETE FROM seguidores WHERE seguidor_id = ? AND seguido_id = ?",
      (seguidor_id, seguido_id))
  conn.commit()


# Funções para dar e remover likes
def dar_like(postagem_id):
  cursor.execute("UPDATE postagens SET likes = likes + 1 WHERE id = ?",
                 (postagem_id, ))
  conn.commit()


def remover_like(postagem_id):
  cursor.execute("UPDATE postagens SET likes = likes - 1 WHERE id = ?",
                 (postagem_id, ))
  conn.commit()


if __name__ == "__main__":
  criar_tabelas()

  while True:
    print("1. Registrar")
    print("2. Login")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
      username = input("Digite um nome de usuário: ")
      password = input("Digite uma senha: ")
      registrar_usuario(username, password)
      print("Usuário registrado com sucesso!")

    elif opcao == "2":
      username = input("Nome de usuário: ")
      password = input("Senha: ")
      user_id = fazer_login(username, password)
      if user_id:
        print("Login bem-sucedido!")
        while True:
          print("1. Publicar uma postagem")
          print("2. Listar postagens")
          print("3. Sair")
          opcao = input("Escolha uma opção: ")

          if opcao == "1":
            conteudo = input("Escreva sua postagem: ")
            criar_postagem(user_id[0], conteudo)
            print("Postagem criada com sucesso!")

          elif opcao == "2":
            postagens = listar_postagens()
            for postagem in postagens:
              print(f"Postagem {postagem[0]} por Usuário {postagem[1]}:")
              print(postagem[2])
              print(f"Likes: {postagem[3]}")
              comentarios = listar_comentarios(postagem[0])
              if comentarios:
                print("Comentários:")
                for comentario in comentarios:
                  print(f"Usuário {comentario[2]}: {comentario[3]}")
              print("\n")

          elif opcao == "3":
            break
      else:
        print("Login falhou. Tente novamente ou registre-se.")

    else:
      break

  conn.close()
