CREATE SCHEMA IF NOT EXISTS avaliacao;
SET search_path = avaliacao, public;

CREATE TABLE bairro (
  codigo_bairro SERIAL PRIMARY KEY,
  nome VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE usuario (
  cpf BIGSERIAL PRIMARY KEY,
  nome VARCHAR(200) NOT NULL,
  email VARCHAR(200) UNIQUE,
  codigo_bairro INT REFERENCES bairro(codigo_bairro) ON DELETE SET NULL,
  criado_em TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE secretaria (
  sigla_secretaria SERIAL PRIMARY KEY,
  nome VARCHAR(150) NOT NULL UNIQUE,
  descricao TEXT
);

CREATE TABLE servico (
  registro_servico SERIAL PRIMARY KEY,
  nome VARCHAR(200) NOT NULL,
  descricao TEXT,
  endereco VARCHAR(300),
  codigo_bairro INT REFERENCES bairro(codigo_bairro) ON DELETE SET NULL,
  sigla_secretaria INT NOT NULL REFERENCES secretaria(sigla_secretaria) ON DELETE CASCADE
);

CREATE TYPE tipo_questao AS ENUM ('escala', 'multipla', 'texto');

CREATE TABLE questao (
  numero_questao SERIAL PRIMARY KEY,
  texto TEXT NOT NULL,
  tipo tipo_questao NOT NULL,
  valor_min INT,
  valor_max INT,
  obrigatoria BOOLEAN DEFAULT true
);

CREATE TABLE opcao (
  codigo_opcao SERIAL PRIMARY KEY,
  letra CHAR(1),
  texto VARCHAR(300) NOT NULL,
  valor_numerico NUMERIC,
  numero_questao INT NOT NULL REFERENCES questao(numero_questao) ON DELETE CASCADE
);

CREATE TABLE avaliacao (
  numero_avaliacao SERIAL PRIMARY KEY,
  titulo VARCHAR(250) NOT NULL,
  descricao TEXT,
  data_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
  data_fim TIMESTAMP WITH TIME ZONE NOT NULL,
  anonimato BOOLEAN DEFAULT false,
  criado_em TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE avaliacao_servico (
  numero_avaliacao INT NOT NULL REFERENCES avaliacao(numero_avaliacao) ON DELETE CASCADE,
  registro_servico INT NOT NULL REFERENCES servico(registro_servico) ON DELETE CASCADE,
  PRIMARY KEY (numero_avaliacao, registro_servico)
);

CREATE TABLE avaliacao_questao (
  numero_avaliacao INT NOT NULL REFERENCES avaliacao(numero_avaliacao) ON DELETE CASCADE,
  numero_questao INT NOT NULL REFERENCES questao(numero_questao) ON DELETE CASCADE,
  ordem INT DEFAULT 1,
  peso NUMERIC DEFAULT 1,
  PRIMARY KEY (numero_avaliacao, numero_questao)
);

CREATE TABLE resposta (
  numero_resposta BIGSERIAL PRIMARY KEY,
  numero_avaliacao INT NOT NULL REFERENCES avaliacao(numero_avaliacao) ON DELETE CASCADE,
  registro_servico INT NOT NULL REFERENCES servico(registro_servico) ON DELETE CASCADE,
  numero_questao INT NOT NULL REFERENCES questao(numero_questao) ON DELETE CASCADE,
  cpf_usuario BIGINT REFERENCES usuario(cpf) ON DELETE SET NULL,
  texto_resposta TEXT,
  codigo_opcao INT REFERENCES opcao(codigo_opcao) ON DELETE SET NULL,
  valor_numerico NUMERIC,
  criado_em TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX idx_resposta_avaliacao_servico ON resposta(numero_avaliacao, registro_servico);
CREATE INDEX idx_resposta_criado ON resposta(criado_em);
CREATE INDEX idx_servico_secretaria ON servico(sigla_secretaria);
