from banco_de_dados.conexao import conectar, fechar_conexao


def listar_vendas():

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
    tbl_vendas.id_venda,
    tbl_clientes.nome_cliente,
    tbl_barbeiros.nome_barbeiro,
    tbl_servicos.nome_servico,
    tbl_vendas.valor_venda,
    tbl_vendas.forma_pagamento
    FROM tbl_vendas

    INNER JOIN tbl_agendamentos
    ON tbl_vendas.id_agendamento = tbl_agendamentos.id_agendamento

    INNER JOIN tbl_clientes
    ON tbl_agendamentos.id_cliente = tbl_clientes.id_cliente

    INNER JOIN tbl_barbeiros
    ON tbl_agendamentos.id_barbeiro = tbl_barbeiros.id_barbeiro

    INNER JOIN tbl_servicos
    ON tbl_agendamentos.id_servico = tbl_servicos.id_servico
    """

    cursor.execute(sql)

    vendas = cursor.fetchall()

    for venda in vendas:

        print(
            f"""
    ID Venda: {venda[0]}
    Cliente: {venda[1]}
    Barbeiro: {venda[2]}
    Serviço: {venda[3]}
    Valor: R${venda[4]}
    Forma de pagamento: {venda[5]}
    """
        )

    cursor.close()
    fechar_conexao(conexao)


def cadastrar_venda():

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        id_agendamento = input("ID do agendamento: ")
        valor = input("Valor da venda: ")
        forma_pagamento = input(
            "Forma de pagamento (pix/debito/credito/dinheiro): "
        )

        cursor.execute(
            "SELECT id_venda FROM tbl_vendas WHERE id_agendamento = %s",
            (id_agendamento,)
        )

        if cursor.fetchone():
            print("Já existe uma venda para esse agendamento.")
            cursor.close()
            fechar_conexao(conexao)
            return

        sql = """
        INSERT INTO tbl_vendas
        (
            id_agendamento,
            valor_venda,
            forma_pagamento
        )
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                id_agendamento,
                valor,
                forma_pagamento
            )
        )

        sql_update = """
        UPDATE tbl_agendamentos
        SET status_agendamento = 'concluido'
        WHERE id_agendamento = %s
        """

        cursor.execute(sql_update, (id_agendamento,))

        conexao.commit()

        print("Venda cadastrada!")

        cursor.close()
        fechar_conexao(conexao)

    except Exception:
        print("Erro ao cadastrar venda. Verifique se o agendamento existe.")

def editar_venda():
    conexao = conectar()
    cursor = conexao.cursor()

    id_venda = input("ID da venda: ")
    valor = input("Novo valor: ")
    forma_pagamento = input("Nova forma de pagamento: ")

    sql = """
    UPDATE tbl_vendas
    SET valor_venda = %s,
        forma_pagamento = %s
    WHERE id_venda = %s
    """

    cursor.execute(
        sql,
        (valor, forma_pagamento, id_venda)
    )

    conexao.commit()

    print("Venda atualizada!")

    cursor.close()
    fechar_conexao(conexao)


def excluir_venda():
    conexao = conectar()
    cursor = conexao.cursor()

    id_venda = input("ID da venda: ")

    cursor.execute(
        "DELETE FROM tbl_vendas WHERE id_venda = %s",
        (id_venda,)
    )

    conexao.commit()

    if cursor.rowcount > 0:
        print("Registro excluído com sucesso!")
    else:
        print("Nenhum registro encontrado com esse ID.")

    print("Venda excluída!")

    cursor.close()
    fechar_conexao(conexao)


def menu():
    while True:
        print("\n===== VENDAS =====")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_venda()
        elif opcao == "2":
            listar_vendas()
        elif opcao == "3":
            editar_venda()
        elif opcao == "4":
            excluir_venda()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")