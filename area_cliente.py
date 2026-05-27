from banco_de_dados.conexao import conectar, fechar_conexao
from datetime import datetime, timedelta


def buscar_id_cliente(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT id_cliente
    FROM tbl_clientes
    WHERE id_usuario = %s
    """

    cursor.execute(sql, (id_usuario,))
    resultado = cursor.fetchone()

    cursor.close()
    fechar_conexao(conexao)

    if resultado:
        return resultado[0]

    return None


def listar_barbeiros():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
    id_barbeiro,
    nome_barbeiro,
    especialidade_barbeiro
    FROM tbl_barbeiros
    """

    cursor.execute(sql)
    barbeiros = cursor.fetchall()

    print("\n===== BARBEIROS =====")

    for barbeiro in barbeiros:
        print(
            f"ID: {barbeiro[0]} | "
            f"Nome: {barbeiro[1]} | "
            f"Especialidade: {barbeiro[2]}"
        )

    cursor.close()
    fechar_conexao(conexao)


def listar_servicos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
    id_servico,
    nome_servico,
    preco_servico,
    duracao_minutos
    FROM tbl_servicos
    """

    cursor.execute(sql)
    servicos = cursor.fetchall()

    print("\n===== SERVIÇOS =====")

    for servico in servicos:
        print(
            f"ID: {servico[0]} | "
            f"Serviço: {servico[1]} | "
            f"Preço: R${servico[2]} | "
            f"Duração: {servico[3]} minutos"
        )

    cursor.close()
    fechar_conexao(conexao)


def ver_meus_agendamentos(id_usuario):
    id_cliente = buscar_id_cliente(id_usuario)

    if id_cliente is None:
        print("Cliente não encontrado.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT
    tbl_agendamentos.id_agendamento,
    tbl_barbeiros.nome_barbeiro,
    tbl_servicos.nome_servico,
    tbl_agendamentos.data_hora,
    tbl_agendamentos.status_agendamento
    FROM tbl_agendamentos

    INNER JOIN tbl_barbeiros
    ON tbl_agendamentos.id_barbeiro = tbl_barbeiros.id_barbeiro

    INNER JOIN tbl_servicos
    ON tbl_agendamentos.id_servico = tbl_servicos.id_servico

    WHERE tbl_agendamentos.id_cliente = %s
    """

    cursor.execute(sql, (id_cliente,))
    agendamentos = cursor.fetchall()

    print("\n===== MEUS AGENDAMENTOS =====")

    if len(agendamentos) == 0:
        print("Você ainda não possui agendamentos.")

    else:
        for agendamento in agendamentos:
            print(
                f"ID: {agendamento[0]} | "
                f"Barbeiro: {agendamento[1]} | "
                f"Serviço: {agendamento[2]} | "
                f"Data/Hora: {agendamento[3]} | "
                f"Status: {agendamento[4]}"
            )

    cursor.close()
    fechar_conexao(conexao)


def criar_agendamento(id_usuario):
    try:
        id_cliente = buscar_id_cliente(id_usuario)

        if id_cliente is None:
            print("Cliente não encontrado.")
            return

        listar_barbeiros()
        id_barbeiro = input("\nDigite o ID do barbeiro: ")

        if id_barbeiro == "":
            print("Informe o ID do barbeiro.")
            return

        listar_servicos()
        id_servico = input("\nDigite o ID do serviço: ")

        if id_servico == "":
            print("Informe o ID do serviço.")
            return

        data = input("Digite a data do agendamento (AAAA-MM-DD): ")

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            print("Data inválida. Use o formato AAAA-MM-DD.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT duracao_minutos FROM tbl_servicos WHERE id_servico = %s",
            (id_servico,)
        )

        resultado_servico = cursor.fetchone()

        if resultado_servico is None:
            print("Serviço não encontrado.")
            cursor.close()
            fechar_conexao(conexao)
            return

        duracao_novo_servico = resultado_servico[0]

        horarios = [
            "09:00:00",
            "10:00:00",
            "11:00:00",
            "13:00:00",
            "14:00:00",
            "15:00:00",
            "16:00:00",
            "17:00:00"
        ]

        horarios_disponiveis = []

        for horario in horarios:
            inicio_novo = datetime.strptime(
                f"{data} {horario}",
                "%Y-%m-%d %H:%M:%S"
            )

            fim_novo = inicio_novo + timedelta(minutes=duracao_novo_servico)

            sql_conflito = """
            SELECT
            tbl_agendamentos.data_hora,
            tbl_servicos.duracao_minutos
            FROM tbl_agendamentos
            INNER JOIN tbl_servicos
            ON tbl_agendamentos.id_servico = tbl_servicos.id_servico
            WHERE tbl_agendamentos.id_barbeiro = %s
            AND DATE(tbl_agendamentos.data_hora) = %s
            AND tbl_agendamentos.status_agendamento = 'agendado'
            """

            cursor.execute(sql_conflito, (id_barbeiro, data))
            agendamentos_existentes = cursor.fetchall()

            conflito = False

            for agendamento in agendamentos_existentes:
                inicio_existente = agendamento[0]
                duracao_existente = agendamento[1]
                fim_existente = inicio_existente + timedelta(minutes=duracao_existente)

                if inicio_novo < fim_existente and fim_novo > inicio_existente:
                    conflito = True
                    break

            if not conflito:
                horarios_disponiveis.append(horario)

        if len(horarios_disponiveis) == 0:
            print("Não há horários disponíveis para esse barbeiro nessa data.")
            cursor.close()
            fechar_conexao(conexao)
            return

        print("\n===== HORÁRIOS DISPONÍVEIS =====")
        for i, horario in enumerate(horarios_disponiveis, start=1):
            print(f"{i} - {horario}")

        opcao_horario = input("Escolha o horário: ")

        if opcao_horario == "":
            print("Escolha um horário.")
            cursor.close()
            fechar_conexao(conexao)
            return

        indice = int(opcao_horario) - 1

        if indice < 0 or indice >= len(horarios_disponiveis):
            print("Horário inválido.")
            cursor.close()
            fechar_conexao(conexao)
            return

        horario_escolhido = horarios_disponiveis[indice]
        data_hora = f"{data} {horario_escolhido}"

        sql_insert = """
        INSERT INTO tbl_agendamentos
        (
            id_cliente,
            id_barbeiro,
            id_servico,
            data_hora,
            status_agendamento
        )
        VALUES (%s, %s, %s, %s, 'agendado')
        """

        cursor.execute(
            sql_insert,
            (
                id_cliente,
                id_barbeiro,
                id_servico,
                data_hora
            )
        )

        conexao.commit()

        print("Agendamento criado com sucesso!")

        cursor.close()
        fechar_conexao(conexao)

    except ValueError:
        print("Escolha inválida. Digite apenas números.")

    except Exception:
        print("Erro ao criar agendamento.")
        print("Verifique se os dados foram preenchidos corretamente.")


def cancelar_agendamento(id_usuario):
    id_cliente = buscar_id_cliente(id_usuario)

    if id_cliente is None:
        print("Cliente não encontrado.")
        return

    ver_meus_agendamentos(id_usuario)

    id_agendamento = input(
        "\nDigite o ID do agendamento que deseja cancelar: "
    )

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE tbl_agendamentos
    SET status_agendamento = 'cancelado'
    WHERE id_agendamento = %s
    AND id_cliente = %s
    """

    cursor.execute(sql, (id_agendamento, id_cliente))
    conexao.commit()

    if cursor.rowcount > 0:
        print("Agendamento cancelado com sucesso!")

    else:
        print("Agendamento não encontrado.")

    cursor.close()
    fechar_conexao(conexao)

def editar_meus_dados(id_usuario):
    try:
        id_cliente = buscar_id_cliente(id_usuario)

        if id_cliente is None:
            print("Cliente não encontrado.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        print("\n===== EDITAR MEUS DADOS =====")
        print("Caso não queira alterar algum dado, informe novamente o valor atual.\n")

        novo_login = input("Novo login: ")
        nova_senha = input("Nova senha: ")
        novo_nome = input("Novo nome: ")
        novo_numero = input("Novo telefone: ")
        novo_email = input("Novo email: ")

        cursor.execute(
            """
            SELECT id_usuario
            FROM tbl_usuarios
            WHERE login_usuario = %s
            AND id_usuario <> %s
            """,
            (novo_login, id_usuario)
        )

        if cursor.fetchone():
            print("Esse login já está em uso.")
            cursor.close()
            fechar_conexao(conexao)
            return

        cursor.execute(
            """
            UPDATE tbl_usuarios
            SET login_usuario = %s,
                senha_usuario = %s
            WHERE id_usuario = %s
            """,
            (novo_login, nova_senha, id_usuario)
        )

        cursor.execute(
            """
            UPDATE tbl_clientes
            SET nome_cliente = %s,
                numero_cliente = %s,
                email_cliente = %s
            WHERE id_cliente = %s
            """,
            (novo_nome, novo_numero, novo_email, id_cliente)
        )

        conexao.commit()

        print("Dados atualizados com sucesso!")

        cursor.close()
        fechar_conexao(conexao)

    except Exception:
        print("Erro ao atualizar dados.")
        

def menu_cliente(id_usuario, nome_login):

    while True:

        print(f"\n===== MENU CLIENTE: {nome_login} =====")
        print("1 - Ver meus agendamentos")
        print("2 - Criar agendamento")
        print("3 - Cancelar agendamento")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            ver_meus_agendamentos(id_usuario)

        elif opcao == "2":
            criar_agendamento(id_usuario)

        elif opcao == "3":
            cancelar_agendamento(id_usuario)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")


def menu_cliente(id_usuario, nome_login):

    while True:

        print(f"\n===== MENU CLIENTE: {nome_login} =====")
        print("1 - Ver meus agendamentos")
        print("2 - Criar agendamento")
        print("3 - Cancelar agendamento")
        print("4 - Editar meus dados")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            ver_meus_agendamentos(id_usuario)

        elif opcao == "2":
            criar_agendamento(id_usuario)

        elif opcao == "3":
            cancelar_agendamento(id_usuario)

        elif opcao == "4":
            editar_meus_dados(id_usuario)

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")