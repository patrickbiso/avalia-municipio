# Projeto: AvaliaMunicípio - Sistema de Avaliação de Serviços Públicos

Este repositório contém o projeto da disciplina de Banco de Dados I, focado no desenvolvimento de um sistema para avaliação de serviços públicos municipais.

---

## 1. Descrição do Sistema

* **Nome:** AvaliaMunicípio
* **Objetivo:** Permitir que cidadãos avaliem serviços públicos (Saúde, Transporte, Educação, Saneamento, etc.), armazenar respostas a questionários de avaliação e gerar relatórios analíticos (médias por secretaria, variação por bairro, evolução temporal, ranking de serviços, etc.).
* **Público-alvo:** Cidadãos, gestores públicos (secretarias), administradores do sistema.

### Requisitos Funcionais Principais

- Cadastrar Secretarias e Serviços (ex.: Secretaria de Saúde -> UBS Centro).
- Criar Avaliações (pesquisas) compostas por Questões reutilizáveis (tipos: escala numérica, múltipla escolha, texto livre).
- Associar uma avaliação a um conjunto de serviços e a um período (data/hora de abertura e fechamento).
- Registrar Respostas de cidadãos para cada questão de uma avaliação aplicada a um serviço (podendo ser anônimas ou nominais, conforme a avaliação).
- Gerar relatórios com consultas SQL que explorem junções, agregações, subconsultas, ranking e janelas.

---

## 2. Fluxo Básico das Funcionalidades

1.  **Administrador** cadastra Secretarias e Serviços.
2.  **Administrador** cria Questões (ex. “Satisfação com atendimento” — escala 1..5).
3.  **Administrador** cria uma Avaliação (ex.: “Pesquisa Outubro 2025 sobre UBSs”), seleciona as questões e os serviços-alvo, e define se a avaliação será anônima.
4.  O **Cidadão** acessa a avaliação para um serviço específico, responde o questionário e submete suas respostas.
5.  O **Sistema** grava as respostas em uma transação e atualiza eventuais métricas.
6.  O **Gestor** solicita relatórios, como média por secretaria, média por bairro, evolução temporal e ranking de serviços.

---

## 3. Relatórios Planejados

- **Média por Secretaria (últimos 6 meses):** Apresenta a média da nota (para questões de escala) agrupada por secretaria.
- **Média por Bairro:** Calcula a média das respostas (por serviço ou por secretaria) filtrada pelo bairro do cidadão.
- **Variação Temporal (mensal):** Mostra a evolução da média mês a mês para um serviço ou secretaria específica.
- **Ranking de Serviços:** Exibe um TOP N de serviços com base na média de satisfação.
- **Comparativo entre Bairros:** Calcula a média global e a compara com a média de cada bairro.
- **Distribuição de Respostas:** Fornece a contagem de respostas por valor (ex: de 1 a 5) para uma questão específica.
- **Relatório Anônimo vs. Nominal:** Apresenta estatísticas separadas para avaliações anônimas e nominais.

---
