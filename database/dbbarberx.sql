CREATE DATABASE barberx;
USE barberx;


CREATE TABLE tbl_clientes (
id_clientes INT AUTO_INCREMENT PRIMARY KEY, 
nome_cliente VARCHAR(100), 
numero_cliente VARCHAR(20),
email_cliente VARCHAR(100)
);  

 CREATE TABLE tbl_barbeiros (
id_barbeiro INT AUTO_INCREMENT PRIMARY KEY, 
nome_barbeiro VARCHAR(100), 
especialidade_barbeiro VARCHAR(100), 
telefone_barbeiro VARCHAR(20)
);

CREATE TABLE tbl_servicos (
id_servico INT AUTO_INCREMENT PRIMARY KEY, 
nome_servico VARCHAR(100), 
descricao_servico VARCHAR(100),
preco_servico DECIMAL(10.2),
duracao_servico TIME 
);

CREATE TABLE tbl_agendamentos (
id_agendamento INT AUTO_INCREMENT PRIMARY KEY, 
datahora_agendamento DATETIME,
status_agendamento ENUM('agendado', 'concluido', 'cancelado') DEFAULT 'agendado'
); 

 CREATE TABLE tbl_vendas(
id_vendas INT AUTO_INCREMENT PRIMARY KEY,
valor_vendas DECIMAL(10.2),
formapagamento_vendas ENUM('pix', 'debito', 'credito', 'dinheiro', 'pagamento') DEFAULT 'pagamento'
);  

CREATE TABLE tbl_usuarios (
id_usuarios INT AUTO_INCREMENT PRIMARY KEY, 
login_usuarios VARCHAR(100) NOT NULL,
senha_usuarios VARCHAR(30) NOT NULL, 
tipo_usuarios BOOL
); 


