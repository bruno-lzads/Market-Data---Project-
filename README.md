# Market Data Pipeline

Pipeline em Python para **coleta, validação, normalização e armazenamento de dados públicos do mercado financeiro**.

O projeto está sendo desenvolvido como estudo prático de engenharia de dados e backend, com foco em arquitetura modular, qualidade de código, testes automatizados e evolução gradual para uma infraestrutura baseada em PostgreSQL, Docker e AWS.

> **Status:** em desenvolvimento ativo.

## Objetivos do projeto

- Consumir dados financeiros de fontes públicas por API
- Validar respostas e tratar erros de integração
- Normalizar dados recebidos
- Persistir dados de mercado em banco relacional
- Registrar execuções de coleta para auditoria e observabilidade
- Automatizar testes com Pytest
- Containerizar a aplicação
- Evoluir o fluxo para processamento assíncrono utilizando AWS SQS

## Arquitetura planejada

```text
Fonte pública
     │
     ▼
Coletor Python
(Requests / API)
     │
     ▼
Validação e normalização
     │
     ▼
PostgreSQL
     │
     ▼
AWS SQS
     │
     ▼
Worker Python
```

A arquitetura será implementada de forma incremental durante o desenvolvimento.

## Tecnologias

### Atualmente

- Python 3.12+
- Pytest
- APIs REST
- Estrutura de pacote com `src/`

### Planejadas

- PostgreSQL
- Docker
- Docker Compose
- AWS SQS
- AWS S3
- AWS CloudWatch
- CI/CD

## Estrutura

```text
.
├── src/
│   └── market_data/
├── tests/
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Ambiente de desenvolvimento

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

Instale o projeto em modo editável com as dependências de desenvolvimento:

```bash
pip install -e ".[dev]"
```

Execute os testes:

```bash
pytest
```

## Princípios adotados

O projeto busca demonstrar práticas utilizadas em aplicações reais, incluindo:

- Separação de responsabilidades
- Configuração externa por variáveis de ambiente
- Tratamento explícito de erros de integração
- Testes unitários
- Evolução incremental da arquitetura
- Documentação das decisões técnicas

## Roadmap

- [x] Estrutura inicial do pacote Python
- [x] Configuração do Pytest
- [x] Cliente inicial para consumo de dados financeiros
- [ ] Camada de persistência PostgreSQL
- [ ] Docker e Docker Compose
- [ ] Publicação de eventos em AWS SQS
- [ ] Worker para processamento assíncrono
- [ ] Observabilidade e logging estruturado
- [ ] Pipeline de CI/CD

## Autor

**Bruno Luiz** — [GitHub](https://github.com/bruno-lzads)
