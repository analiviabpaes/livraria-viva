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
('Noites Brancas', 'Fiódor Dostoiévski', 27.90, 10, 2),
('Orgulho e Preconceito', 'Jane Austen', 34.90, 10, 2),
('Dom Casmurro', 'Machado de Assis', 27.90, 10, 2),
('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 24.90, 10, 3),
('A Ilha do Tesouro', 'Robert Louis Stevenson', 31.90, 10, 3),
('Viagem ao Centro da Terra', 'Júlio Verne', 29.90, 10, 3),
('Drácula', 'Bram Stoker', 39.90, 10, 4),
('O Silêncio dos Inocentes', 'Thomas Harris', 41.90, 10, 4),
('O Código Da Vinci', 'Dan Brown', 44.90, 10, 4),
('É Assim que Acaba', 'Colleen Hoover', 42.90, 10, 1),
('Para Todos os Garotos que Já Amei', 'Jenny Han', 38.90, 10, 1);