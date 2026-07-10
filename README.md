# 🚀 RPA Web Service com Playwright

# ATIVAR O TUNNEL
cloudflared.exe  tunnel --url http://localhost:5000

# RODAR UV
uv run uvicorn app.main:app --reload

# ESTRUTURA DO PROJETO

# Diretórios principais

| Diretório | Responsabilidade |
|------------|------------------|
| `api/` | Camada de interface HTTP. Contém rotas, dependências e middlewares da aplicação. |
| `app/` | Camada de aplicação. Contém DTOs e casos de uso responsáveis por orquestrar as regras de negócio. |
| `core/` | Componentes compartilhados da aplicação, como logging, tratamento de exceções, formulários e recursos globais. |
| `domain/` | Núcleo do negócio. Contém entidades e contratos de repositórios independentes de tecnologia. |
| `frontend/` | Recursos da interface web, incluindo templates HTML, arquivos estáticos e componentes visuais. |
| `infrastructure/` | Implementações concretas e integrações externas, como banco de dados, e-mail, Teams, arquivos e serviços auxiliares. |
| `jobs/` | Rotinas automatizadas e scripts executáveis de processamento. |
| `logs/` | Arquivos gerados durante a execução da aplicação, incluindo auditorias, erros e logs operacionais. |
| `models/` | Modelos de domínio e estruturas de dados utilizadas pelos processos internos da aplicação. |
| `pipe/` | Estrutura base para construção e execução de pipelines de processamento de dados. |
| `settings/` | Configurações centralizadas da aplicação, parâmetros de execução e regras de negócio compartilhadas. |
| `docs/` | Documentação técnica, diagramas e materiais de apoio ao desenvolvimento. |
| `tests/` | Testes automatizados e arquivos auxiliares para validação do sistema. |

---

# Detalhamento por diretório

## `api/`

Responsável por receber requisições HTTP e encaminhá-las para a camada de aplicação.

### Estrutura

- `routes/`
  - Define os endpoints da aplicação.
  - Não deve conter regra de negócio.
  - Apenas recebe a requisição e chama os casos de uso.

- `dependencies/`
  - Centraliza a criação e injeção de dependências.
  - Utilizado para fornecer repositórios, serviços e casos de uso para as rotas.

- `middlewares/`
  - Contém middlewares utilizados durante o ciclo da requisição.
  - Exemplo: observabilidade, logging e monitoramento.

---

## `app/`

Camada responsável por coordenar as operações do sistema.

### Estrutura

- `dto/`
  - Modelos de entrada e saída da aplicação.
  - Utilizados para validação e transporte de dados.

- `use_cases/`
  - Implementa os casos de uso da aplicação.
  - Orquestra entidades, repositórios e serviços para executar uma funcionalidade específica.

- `main.py`
  - Ponto de entrada da aplicação.

---

## `core/`

Contém recursos compartilhados utilizados por toda a aplicação.

### Estrutura

- `exceptions/`
  - Exceções customizadas e handlers globais.

- `logging/`
  - Configuração do sistema de logs.
  - Contexto de execução.
  - Classes auxiliares para auditoria e rastreabilidade.

- `database.py`
  - Configurações globais de acesso ao banco.

- `forms.py`
  - Estruturas de formulários utilizadas pela interface web.

- `models.py`
  - Modelos compartilhados utilizados por múltiplos módulos.

---

## `domain/`

Representa o núcleo do negócio.

### Estrutura

- `entities/`
  - Entidades que representam conceitos do negócio.
  - Exemplo: `User`, `Sector`.

- `repositories/`
  - Contratos (interfaces) de acesso aos dados.
  - Não possuem implementação técnica.
  - Definem apenas o comportamento esperado.

---

## `frontend/`

Contém todos os recursos da interface web.

### Estrutura

- `static/`
  - Arquivos estáticos da aplicação.

  - `css/`
    - Folhas de estilo.

  - `js/`
    - Scripts JavaScript.

  - `img/`
    - Imagens e ícones.

- `templates/`
  - Templates HTML renderizados pela aplicação.

- `components/`
  - Componentes reutilizáveis da interface.

- `emails/`
  - Templates HTML utilizados em envios de e-mail.

- `teams/`
  - Templates JSON utilizados para mensagens do Microsoft Teams.

---

## `infrastructure/`

Contém implementações concretas e integrações externas.

### Estrutura

- `database/`
  - Clientes de banco de dados.
  - Implementações concretas dos repositórios definidos no domínio.

- `dataframes/`
  - Manipulação e gerenciamento de DataFrames.

- `email/`
  - Envio de e-mails.
  - Renderização de templates.

- `files/`
  - Operações de leitura, escrita e gerenciamento de arquivos.

- `teams/`
  - Integração com Microsoft Teams.

- `templates/`
  - Templates utilizados por processos internos.

- `service/`
  - Serviços técnicos reutilizáveis.
  - Conversão de dados.
  - Processamento de DataFrames.
  - Leitura e exportação de arquivos.
  - Regras específicas de automações.

---

## `jobs/`

Contém automações executáveis de forma independente.

### Recebe

- Scripts de execução.
- Rotinas agendadas.
- Processos batch.
- Entradas de pipelines.

Exemplo:

- `extract_pending_invoice_transit.py`

---

## `logs/`

Armazena informações geradas durante a execução da aplicação.

### Estrutura

- `audit/`
  - Auditoria de processos.

- `errors/`
  - Registro de falhas e exceções.

- `executions/`
  - Histórico de execuções e métricas operacionais.

---

## `models/`

Contém modelos de domínio utilizados pelos processos internos.

### Estrutura

- `data/`
  - Estruturas auxiliares de dados.

- `ilpn/`
  - Modelos relacionados ao domínio de cobrança e processamento de ILPN.

### Recebe

- Dataclasses.
- Entidades específicas de automações.
- Value Objects.
- Contratos de dados internos.

---

## `pipe/`

Estrutura base para construção de pipelines.

### Estrutura

- `base/`
  - Classes base utilizadas pelos pipelines.

- `validators/`
  - Validadores de dados utilizados durante o processamento.

### Recebe

- Contextos de execução.
- Resultados de pipeline.
- Validações.
- Componentes reutilizáveis de ETL.

---

## `settings/`

Centraliza todas as configurações da aplicação.

### Recebe

- Variáveis de configuração.
- Caminhos do sistema.
- Regras de negócio compartilhadas.
- Configurações de automação.
- Configurações de pipelines.

### Estrutura

- `settings.py`
- `paths.py`
- `pipe_config.py`
- `chromium_settings.py`
- `regras_pix.py`

---

## `docs/`

Documentação técnica do projeto.

### Recebe

- Diagramas.
- Fluxogramas.
- Modelagens.
- Documentação arquitetural.

---

## `tests/`

Testes automatizados da aplicação.

### Recebe

- Testes unitários.
- Testes de integração.
- Mocks.
- Fixtures.



# Extração de Relatório de Notas Fiscais Pendentes

settings/pcomm_settings.py: definir sessão A e timeouts.

infrastructure/pcomm/client.py: conectar, validar sessão, enviar teclas e ler texto.

infrastructure/pcomm/session_validator.py: validar explicitamente se a sessão A está aberta.

infrastructure/pcomm/screen_parser.py: extrair os campos que aparecem na tela.

domain/entities/registro_pcomm.py: representar a linha do Parquet e os dados enriquecidos.

infrastructure/files/parquet_repository_impl.py: ler as 3 colunas e salvar o resultado.

infrastructure/service/enriquecimento_service.py: aplicar a regra de negócio de enriquecimento.

app/use_cases/processar_parquet_pcomm.py: orquestrar a leitura, consulta ao PCOMM e escrita do Parquet.