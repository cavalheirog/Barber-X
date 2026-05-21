from banco_de_dados.conexao import conectar, fechar_conexao

def listar_barbeiros():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tbl_barbeiros")

    barbeiros = cursor.fetchall()

    for barbeiro in barbeiros:

        print(
            f"""
    ID Barbeiro: {barbeiro[0]}
    Nome: {barbeiro[1]}
    Especialidade: {barbeiro[2]}
    Telefone: {barbeiro[3]}
    """
        )

    cursor.close()
    fechar_conexao(conexao)


def cadastrar_barbeiro():

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        nome = input("Nome: ")
        especialidade = input("Especialidade: ")
        telefone = input("Telefone: ")

        cursor.execute(
            "SELECT id_barbeiro FROM tbl_barbeiros WHERE nome_barbeiro = %s",
            (nome,)
        )

        if cursor.fetchone():
            print("Já existe um barbeiro com esse nome.")
            cursor.close()
            fechar_conexao(conexao)
            return

        sql = """
        INSERT INTO tbl_barbeiros
        (
            nome_barbeiro,
            especialidade_barbeiro,
            telefone_barbeiro
        )
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                nome,
                especialidade,
                telefone
            )
        )

        conexao.commit()

        print("Barbeiro cadastrado!")

        cursor.close()
        fechar_conexao(conexao)

    except Exception:
        print("Erro ao cadastrar barbeiro.")


def editar_barbeiro():
    conexao = conectar()
    cursor = conexao.cursor()

    id_barbeiro = input("ID do barbeiro: ")
    nome = input("Novo nome: ")
    especialidade = input("Nova especialidade: ")
    telefone = input("Novo telefone: ")

    sql = """
    UPDATE tbl_barbeiros
    SET nome_barbeiro = %s,
    especialidade_barbeiro = %s,
    telefone_barbeiro = %s
    WHERE id_barbeiro = %s
    """

    cursor.execute(sql, (nome, especialidade, telefone, id_barbeiro))
    conexao.commit()

    print("Barbeiro atualizado!")

    cursor.close()
    fechar_conexao(conexao)


def excluir_barbeiro():
    conexao = conectar()
    cursor = conexao.cursor()

    id_barbeiro = input("ID do barbeiro: ")

    cursor.execute(
        "DELETE FROM tbl_barbeiros WHERE id_barbeiro = %s",
        (id_barbeiro,)
    )

    conexao.commit()

    if cursor.rowcount > 0:
        print("Registro excluído com sucesso!")
    else:
        print("Nenhum registro encontrado com esse ID.")

    print("Barbeiro excluído!")

    cursor.close()
    fechar_conexao(conexao)


def menu():
    while True:
        print("\n===== BARBEIROS =====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_barbeiro()
        elif opcao == "2":
            listar_barbeiros()
        elif opcao == "3":
            editar_barbeiro()
        elif opcao == "4":
            excluir_barbeiro()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")