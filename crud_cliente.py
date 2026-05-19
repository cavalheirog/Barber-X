from banco_de_dados.conexao import conectar, fechar_conexao

def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tbl_clientes")
    for cliente in cursor.fetchall():
        print(cliente)

    cursor.close()
    fechar_conexao(conexao)


def cadastrar_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    id_usuario = input("ID do usuário: ")
    nome = input("Nome: ")
    numero = input("Número: ")
    email = input("Email: ")

    sql = """
    INSERT INTO tbl_clientes
    (id_usuario, nome_cliente, numero_cliente, email_cliente)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (id_usuario, nome, numero, email))
    conexao.commit()

    print("Cliente cadastrado!")

    cursor.close()
    fechar_conexao(conexao)


def editar_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    id_cliente = input("ID do cliente: ")
    nome = input("Novo nome: ")
    numero = input("Novo número: ")
    email = input("Novo email: ")

    sql = """
    UPDATE tbl_clientes
    SET nome_cliente = %s,
        numero_cliente = %s,
        email_cliente = %s
    WHERE id_cliente = %s
    """

    cursor.execute(sql, (nome, numero, email, id_cliente))
    conexao.commit()

    print("Cliente atualizado!")

    cursor.close()
    fechar_conexao(conexao)


def excluir_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    id_cliente = input("ID do cliente: ")

    cursor.execute(
        "DELETE FROM tbl_clientes WHERE id_cliente = %s",
        (id_cliente,)
    )

    conexao.commit()

    if cursor.rowcount > 0:
        print("Registro excluído com sucesso!")
    else:
        print("Nenhum registro encontrado com esse ID.")

    print("Cliente excluído!")

    cursor.close()
    fechar_conexao(conexao)


def menu():
    while True:
        print("\n===== CLIENTES =====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            editar_cliente()
        elif opcao == "4":
            excluir_cliente()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")