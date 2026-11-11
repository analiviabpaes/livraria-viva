INSERT INTO categoria (nome) VALUES ('Romance'), ('Clássico'), ('Aventura'), ('Suspense');

INSERT INTO usuario (nome, email, senha) VALUES
('Administrador', 'admin@livrariaviva.com', 'scrypt:32768:8:1$Gv7ODcEpIn9Jr0Q8$7a940e2889a46e6edb347946fae079534329b49122f4caec39a86948863d09b8a4a7af13d116f6201bd1b06913f082edd7848e362922222e416ba30c2905a746'),
('Carlos Silva', 'carlos@email.com', 'scrypt:32768:8:1$Gv7ODcEpIn9Jr0Q8$7a940e2889a46e6edb347946fae079534329b49122f4caec39a86948863d09b8a4a7af13d116f6201bd1b06913f082edd7848e362922222e416ba30c2905a746');

INSERT INTO livro (titulo, autor, preco, estoque, id_categoria) VALUES
('A Hipótese do Amor', 'Ali Hazelwood', 39.90, 10, 1),
('Vidas Secas', 'Graciliano Ramos', 29.90, 10, 2),
('Moby Dick', 'Herman Melville', 45.00, 10, 3),
('A Metamorfose', 'Franz Kafka', 25.00, 10, 2),
('Dias Perfeitos', 'Raphael Montes', 34.90, 10, 4),
('Jantar Secreto', 'Raphael Montes', 42.50, 10, 4),
('Cartas ao Pai', 'Franz Kafka', 29.90, 10, 2),
('Memórias Póstumas de Brás Cubas', 'Machado de Assis', 32.90, 10, 2),
('O Sol é para Todos', 'Harper Lee', 49.90, 10, 2),
('Noites Brancas', 'Fiódor Dostoiévski', 27.90, 10, 2);