CREATE DATABASE IF NOT EXISTS barberx;
USE barberx;

CREATE TABLE IF NOT EXISTS tbl_usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    login_usuario VARCHAR(100) NOT NULL,
    senha_usuario VARCHAR(30) NOT NULL,
    tipo_usuario ENUM('admin', 'cliente') DEFAULT 'cliente'
);

CREATE TABLE IF NOT EXISTS tbl_clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    nome_cliente VARCHAR(100) NOT NULL,
    numero_cliente VARCHAR(20),
    email_cliente VARCHAR(100),

    FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario)
);

CREATE TABLE IF NOT EXISTS tbl_barbeiros (
    id_barbeiro INT AUTO_INCREMENT PRIMARY KEY,
    nome_barbeiro VARCHAR(100) NOT NULL,
    especialidade_barbeiro VARCHAR(100),
    telefone_barbeiro VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS tbl_servicos (
    id_servico INT AUTO_INCREMENT PRIMARY KEY,
    nome_servico VARCHAR(100) NOT NULL,
    descricao_servico VARCHAR(150),
    preco_servico DECIMAL(10,2) NOT NULL,
    duracao_minutos INT
);

CREATE TABLE IF NOT EXISTS tbl_agendamentos (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_barbeiro INT NOT NULL,
    id_servico INT NOT NULL,
    data_hora DATETIME NOT NULL,
    status_agendamento ENUM('agendado', 'concluido', 'cancelado') DEFAULT 'agendado',

    FOREIGN KEY (id_cliente) REFERENCES tbl_clientes(id_cliente),
    FOREIGN KEY (id_barbeiro) REFERENCES tbl_barbeiros(id_barbeiro),
    FOREIGN KEY (id_servico) REFERENCES tbl_servicos(id_servico)
);

CREATE TABLE IF NOT EXISTS tbl_vendas (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_agendamento INT NOT NULL,
    valor_venda DECIMAL(10,2) NOT NULL,
    forma_pagamento ENUM('pix', 'debito', 'credito', 'dinheiro') NOT NULL,

    FOREIGN KEY (id_agendamento) REFERENCES tbl_agendamentos(id_agendamento)
);