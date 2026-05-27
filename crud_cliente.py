from banco_de_dados.conexao import conectar, fechar_conexao

def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
        tbl_clientes.id_cliente,
        tbl_usuarios.id_usuario,
        tbl_usuarios.login_usuario,
        tbl_clientes.nome_cliente,
        tbl_clientes.numero_cliente,
        tbl_clientes.email_cliente
    FROM tbl_clientes
    INNER JOIN tbl_usuarios
    ON tbl_clientes.id_usuario = tbl_usuarios.id_usuario
    """

    cursor.execute(sql)
    clientes = cursor.fetchall()

    print("\n===== CLIENTES =====")

    for cliente in clientes:

        print(
        f"""
    ID Cliente: {cliente[0]}
    ID Usuário: {cliente[1]}
    Login: {cliente[2]}
    Nome: {cliente[3]}
    Telefone: {cliente[4]}
    Email: {cliente[5]}
    """
    )

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


def alterar_senha():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        id_usuario = input("ID do usuário: ")
        nova_senha = input("Nova senha: ")

        sql = """
        UPDATE tbl_usuarios
        SET senha_usuario = %s
        WHERE id_usuario = %s
        """

        cursor.execute(sql, (nova_senha, id_usuario))
        conexao.commit()

        if cursor.rowcount > 0:
            print("Senha alterada com sucesso!")
        else:
            print("Usuário não encontrado.")

        cursor.close()
        fechar_conexao(conexao)

    except Exception:
        print("Erro ao alterar senha.")


def excluir_cliente():
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        id_cliente = input("ID do cliente: ")

        cursor.execute(
            "SELECT id_usuario FROM tbl_clientes WHERE id_cliente = %s",
            (id_cliente,)
        )

        resultado = cursor.fetchone()

        if resultado is None:
            print("Cliente não encontrado.")
            cursor.close()
            fechar_conexao(conexao)
            return

        id_usuario = resultado[0]

        cursor.execute(
            """
            SELECT id_agendamento
            FROM tbl_agendamentos
            WHERE id_cliente = %s
            AND status_agendamento = 'agendado'
        """,
            (id_cliente,)
        )

        agendamento = cursor.fetchone()

        if agendamento:
            print("Não é possível excluir este cliente.")
            print("Existe agendamento vinculado a ele.")
            cursor.close()
            fechar_conexao(conexao)
            return

        cursor.execute(
            "DELETE FROM tbl_clientes WHERE id_cliente = %s",
            (id_cliente,)
        )

        cursor.execute(
            "DELETE FROM tbl_usuarios WHERE id_usuario = %s",
            (id_usuario,)
        )

        conexao.commit()

        print("Cliente e usuário excluídos!")

        cursor.close()
        fechar_conexao(conexao)

    except Exception:
        print("Erro ao excluir cliente.")


def menu():
    while True:
        print("\n===== USUÁRIOS E CLIENTES =====")
        print("1 - Listar clientes")
        print("2 - Editar dados do cliente")
        print("3 - Alterar senha do cliente")
        print("4 - Excluir cliente e usuário")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            listar_clientes()
        elif opcao == "2":
            editar_cliente()
        elif opcao == "3":
            alterar_senha()
        elif opcao == "4":
            excluir_cliente()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")