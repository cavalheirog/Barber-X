from banco_de_dados.conexao import conectar, fechar_conexao

def listar_servicos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tbl_servicos")
    for servico in cursor.fetchall():
        print(servico)

    cursor.close()
    fechar_conexao(conexao)


def cadastrar_servico():

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        nome = input("Nome do serviço: ")
        descricao = input("Descrição: ")
        preco = input("Preço: ")
        duracao = input("Duração em minutos: ")

        cursor.execute(
            "SELECT id_servico FROM tbl_servicos WHERE nome_servico = %s",
            (nome,)
        )

        if cursor.fetchone():
            print("Já existe um serviço com esse nome.")
            cursor.close()
            fechar_conexao(conexao)
            return

        sql = """
        INSERT INTO tbl_servicos
        (
            nome_servico,
            descricao_servico,
            preco_servico,
            duracao_minutos
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                nome,
                descricao,
                preco,
                duracao
            )
        )

        conexao.commit()

        print("Serviço cadastrado!")

        cursor.close()
        fechar_conexao(conexao)

    except Exception:
        print("Erro ao cadastrar serviço.")


def editar_servico():
    conexao = conectar()
    cursor = conexao.cursor()

    id_servico = input("ID do serviço: ")
    nome = input("Novo nome: ")
    descricao = input("Nova descrição: ")
    preco = input("Novo preço: ")
    duracao = input("Nova duração: ")

    sql = """
    UPDATE tbl_servicos
    SET nome_servico = %s,
        descricao_servico = %s,
        preco_servico = %s,
        duracao_minutos = %s
    WHERE id_servico = %s
    """

    cursor.execute(sql, (nome, descricao, preco, duracao, id_servico))
    conexao.commit()

    print("Serviço atualizado!")

    cursor.close()
    fechar_conexao(conexao)


def excluir_servico():
    conexao = conectar()
    cursor = conexao.cursor()

    id_servico = input("ID do serviço: ")

    cursor.execute(
        "DELETE FROM tbl_servicos WHERE id_servico = %s",
        (id_servico,)
    )

    conexao.commit()

    if cursor.rowcount > 0:
        print("Registro excluído com sucesso!")
    else:
        print("Nenhum registro encontrado com esse ID.")

    print("Serviço excluído!")

    cursor.close()
    fechar_conexao(conexao)


def menu():
    while True:
        print("\n===== SERVIÇOS =====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_servico()
        elif opcao == "2":
            listar_servicos()
        elif opcao == "3":
            editar_servico()
        elif opcao == "4":
            excluir_servico()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")