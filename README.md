# Barber-X

Sistema de agendamento para barbearias desenvolvido em Python e MySQL.

## Sobre o Projeto

O Barber-X é um sistema CRUD voltado para o gerenciamento de uma barbearia.

O projeto possui área de administrador e área de cliente, permitindo o controle de usuários, clientes, barbeiros, serviços, agendamentos e vendas.

## Funcionalidades

### Área do Cliente

* Cadastro de clientes
* Login de clientes
* Visualização dos próprios agendamentos
* Criação de agendamentos
* Cancelamento de agendamentos
* Edição dos dados da conta
* Exclusão da própria conta
* Validação de horários disponíveis
* Geração de horários disponíveis para agendamento
* Controle de conflito de horários com base na duração dos serviços

### Área Administrativa

* Gerenciamento de clientes e usuários
* Gerenciamento de barbeiros
* Gerenciamento de serviços
* Gerenciamento de agendamentos
* Gerenciamento de vendas
* Alteração automática do status do agendamento ao registrar uma venda

## Tecnologias Utilizadas

* Python
* MySQL
* Git/GitHub

## Banco de Dados

O banco de dados utiliza tabelas relacionadas com chaves primárias e estrangeiras, garantindo a integridade das informações entre usuários, clientes, barbeiros, serviços, agendamentos e vendas.

## Como Executar

1. Executar o script de criação do banco de dados:

`banco_de_dados/criacao_de_schema_e_tabelas.sql`

2. Executar o script de inserção de dados:

`banco_de_dados/insercao_de_dados.sql`

3. Configurar a conexão com o MySQL no arquivo:

`banco_de_dados/conexao.py`

4. Executar o sistema:

`main.py`

## Integrantes

* Gabriel Cavalheiro Sousa
* Guilherme Castro Campos
* Kauã Henrique Santos Oliveira
* Pedro Gabriel Padilha
* Ray Reis Sena
