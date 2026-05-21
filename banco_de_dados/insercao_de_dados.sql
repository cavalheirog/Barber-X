USE barberx;

-- USUARIOS
INSERT INTO tbl_usuarios
(login_usuario, senha_usuario, tipo_usuario)
VALUES
('admin', 'admin', 'admin'),
('cliente', 'cliente', 'cliente'),
('felipe', '1234', 'cliente'),
('anderson', '1234', 'cliente'),
('lucas', '1234', 'cliente');


-- CLIENTES
INSERT INTO tbl_clientes
(id_usuario, nome_cliente, numero_cliente, email_cliente)
VALUES
(2, 'Marcos Lima', '11999999999', 'marcos@gmail.com'),
(3, 'Felipe Souza', '11988888888', 'felipe@gmail.com'),
(4, 'Anderson Silva', '11977777777', 'anderson@gmail.com'),
(5, 'Lucas Pereira', '11966666666', 'lucas@gmail.com');


-- BARBEIROS
INSERT INTO tbl_barbeiros
(nome_barbeiro, especialidade_barbeiro, telefone_barbeiro)
VALUES
('Guilherme', 'Degrade', '11955555555'),
('Fernando', 'Barba', '11944444444'),
('Eduardo', 'Social', '11933333333');


-- SERVICOS
INSERT INTO tbl_servicos
(nome_servico, descricao_servico, preco_servico, duracao_minutos)
VALUES
('Corte Degrade', 'Corte degrade completo', 35.00, 40),
('Barba', 'Aparar e modelar barba', 20.00, 25),
('Corte Social', 'Corte social tradicional', 30.00, 35),
('Corte + Barba', 'Combo corte e barba', 50.00, 60);


-- AGENDAMENTOS
INSERT INTO tbl_agendamentos
(id_cliente, id_barbeiro, id_servico, data_hora, status_agendamento)
VALUES
(1, 1, 1, '2026-05-20 14:00:00', 'agendado'),
(2, 2, 2, '2026-05-20 15:00:00', 'concluido'),
(3, 3, 3, '2026-05-21 16:30:00', 'agendado'),
(4, 1, 4, '2026-05-22 17:00:00', 'cancelado');


-- VENDAS
INSERT INTO tbl_vendas
(id_agendamento, valor_venda, forma_pagamento)
VALUES
(2, 20.00, 'pix'),
(3, 30.00, 'debito'),
(4, 50.00, 'credito');