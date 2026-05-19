from banco_de_dados.conexao import conectar, fechar_conexao


def listar_agendamentos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
        tbl_agendamentos.id_agendamento,
        tbl_clientes.nome_cliente,
        tbl_barbeiros.nome_barbeiro,
        tbl_servicos.nome_servico,
        tbl_agendamentos.data_hora,
        tbl_agendamentos.status_agendamento
    FROM tbl_agendamentos
    INNER JOIN tbl_clientes
    ON tbl_agendamentos.id_cliente = tbl_clientes.id_cliente
    INNER JOIN tbl_barbeiros
    ON tbl_agendamentos.id_barbeiro = tbl_barbeiros.id_barbeiro
    INNER JOIN tbl_servicos
    ON tbl_agendamentos.id_servico = tbl_servicos.id_servico
    """

    cursor.execute(sql)
    agendamentos = cursor.fetchall()

    for agendamento in agendamentos:
        print(agendamento)

    cursor.close()
    fechar_conexao(conexao)


def cadastrar_agendamento():
    conexao = conectar()
    cursor = conexao.cursor()

    id_cliente = input("ID do cliente: ")
    id_barbeiro = input("ID do barbeiro: ")
    id_servico = input("ID do serviço: ")
    data_hora = input("Data e hora (AAAA-MM-DD HH:MM:SS): ")
    status = input("Status (agendado/concluido/cancelado): ")

    sql = """
    INSERT INTO tbl_agendamentos
    (id_cliente, id_barbeiro, id_servico, data_hora, status_agendamento)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (id_cliente, id_barbeiro, id_servico, data_hora, status)
    )

    conexao.commit()

    print("Agendamento cadastrado!")

    cursor.close()
    fechar_conexao(conexao)


def editar_agendamento():
    conexao = conectar()
    cursor = conexao.cursor()

    id_agendamento = input("ID do agendamento: ")

    id_cliente = input("Novo ID do cliente: ")
    id_barbeiro = input("Novo ID do barbeiro: ")
    id_servico = input("Novo ID do serviço: ")
    data_hora = input("Nova data e hora: ")
    status = input("Novo status: ")

    sql = """
    UPDATE tbl_agendamentos
    SET id_cliente = %s,
        id_barbeiro = %s,
        id_servico = %s,
        data_hora = %s,
        status_agendamento = %s
    WHERE id_agendamento = %s
    """

    cursor.execute(
        sql,
        (
            id_cliente,
            id_barbeiro,
            id_servico,
            data_hora,
            status,
            id_agendamento
        )
    )

    conexao.commit()

    print("Agendamento atualizado!")

    cursor.close()
    fechar_conexao(conexao)


def excluir_agendamento():
    conexao = conectar()
    cursor = conexao.cursor()

    id_agendamento = input("ID do agendamento: ")

    cursor.execute(
        "DELETE FROM tbl_agendamentos WHERE id_agendamento = %s",
        (id_agendamento,)
    )

    conexao.commit()

    if cursor.rowcount > 0:
        print("Registro excluído com sucesso!")
    else:
        print("Nenhum registro encontrado com esse ID.")

    print("Agendamento excluído!")

    cursor.close()
    fechar_conexao(conexao)


def menu():
    while True:
        print("\n===== AGENDAMENTOS =====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_agendamento()
        elif opcao == "2":
            listar_agendamentos()
        elif opcao == "3":
            editar_agendamento()
        elif opcao == "4":
            excluir_agendamento()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")