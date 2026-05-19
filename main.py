import crud_cliente
import crud_barbeiro
import crud_servicos
import crud_agendamentos
import crud_vendas
import area_cliente

from banco_de_dados.conexao import conectar, fechar_conexao


def login():
    conexao = conectar()
    cursor = conexao.cursor()

    login_usuario = input("Login: ")
    senha_usuario = input("Senha: ")

    sql = """
    SELECT id_usuario, login_usuario, tipo_usuario
    FROM tbl_usuarios
    WHERE login_usuario = %s AND senha_usuario = %s
    """

    cursor.execute(sql, (login_usuario, senha_usuario))
    usuario = cursor.fetchone()

    cursor.close()
    fechar_conexao(conexao)

    return usuario


def cadastrar_usuario_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n===== CADASTRO DE CLIENTE =====")
    login_usuario = input("Crie um login: ")
    senha_usuario = input("Crie uma senha: ")
    nome_cliente = input("Nome completo: ")
    numero_cliente = input("Telefone: ")
    email_cliente = input("Email: ")

    sql_verificar = """
    SELECT id_usuario
    FROM tbl_usuarios
    WHERE login_usuario = %s
"""

    cursor.execute(sql_verificar, (login_usuario,))
    usuario_existente = cursor.fetchone()

    if usuario_existente:
        print("Já existe um usuário com esse login.")
    cursor.close()
    fechar_conexao(conexao)
    return

    sql_usuario = """
    INSERT INTO tbl_usuarios
    (login_usuario, senha_usuario, tipo_usuario)
    VALUES (%s, %s, 'cliente')
    """

    cursor.execute(sql_usuario, (login_usuario, senha_usuario))
    conexao.commit()

    id_usuario = cursor.lastrowid

    sql_cliente = """
    INSERT INTO tbl_clientes
    (id_usuario, nome_cliente, numero_cliente, email_cliente)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql_cliente, (id_usuario, nome_cliente, numero_cliente, email_cliente))
    conexao.commit()

    print("Cliente cadastrado com sucesso!")

    cursor.close()
    fechar_conexao(conexao)


def menu_admin():
    while True:
        print("\n===== MENU ADMIN =====")
        print("1 - Clientes")
        print("2 - Barbeiros")
        print("3 - Serviços")
        print("4 - Agendamentos")
        print("5 - Vendas")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            crud_cliente.menu()
        elif opcao == "2":
            crud_barbeiro.menu()
        elif opcao == "3":
            crud_servicos.menu()
        elif opcao == "4":
            crud_agendamentos.menu()
        elif opcao == "5":
            crud_vendas.menu()
        elif opcao == "0":
            break 
        else:
            print("Opção inválida.")


def menu_inicial():
    while True:
        print("\n===== BARBER-X =====")
        print("1 - Entrar")
        print("2 - Cadastrar cliente")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            usuario = login()

            if usuario is None:
                print("Login ou senha inválidos.")
            else:
                id_usuario = usuario[0]
                nome_login = usuario[1]
                tipo_usuario = usuario[2]

                if tipo_usuario == "admin":
                    menu_admin()
                elif tipo_usuario == "cliente":
                    area_cliente.menu_cliente(id_usuario, nome_login)

        elif opcao == "2":
            cadastrar_usuario_cliente()

        elif opcao == "0":
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida.")


menu_inicial()