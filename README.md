# 🚀 RPA Web Service com Playwright

Este projeto transforma uma automação local (RPA) em um serviço web centralizado, onde usuários podem disparar execuções diretamente pelo navegador, enquanto a automação roda em um servidor.

---

## 🧠 Visão Geral

A aplicação permite que usuários:

* Acessem uma interface web
* Façam login
* Disparem execuções de automação (RPA)
* Recebam o resultado da execução

Toda a automação é executada no servidor utilizando **Playwright**, sem depender do ambiente do usuário.

---

## 🏗️ Arquitetura

A aplicação segue um modelo desacoplado com fila de tarefas:

```
[ Frontend (Browser) ]
        ↓
[ Backend API ]
        ↓
[ Fila (Redis) ]
        ↓
[ Worker ]
        ↓
[ Playwright (Automação) ]
```

---

## ⚙️ Tecnologias utilizadas

### Backend

* Python 3.10+
* FastAPI
* Uvicorn

### Automação

* Playwright

### Fila de tarefas

* **Redis**
* Celery (ou RQ como alternativa)

### Infra (local)

* Windows (servidor local)
* Opcional: Docker

---

## 📁 Estrutura do Projeto

```
rpa-web-service/
│
├── app/
│   ├── main.py              # API FastAPI
│   ├── routes/
│   │   └── automation.py
│   ├── services/
│   │   └── rpa_service.py
│   └── models/
│
├── worker/
│   └── worker.py           # Worker Celery
│
├── tasks/
│   └── automation_task.py
│
├── playwright/
│   └── scripts/
│       └── example.py      # Script de automação
│
├── requirements.txt
└── README.md
```

---

## 🔄 Fluxo de Execução

1. Usuário acessa o sistema via navegador
2. Realiza login
3. Clica em "Executar Automação"
4. O frontend envia requisição para a API
5. A API registra uma tarefa na fila (Redis)
6. O worker consome a tarefa
7. O Playwright executa a automação
8. O resultado é salvo e retornado ao usuário

---

## 🚀 Setup do Projeto

### 1. Clonar repositório

```bash
git clone https://github.com/seu-usuario/rpa-web-service.git
cd rpa-web-service
```

---

### 2. Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Instalar browsers do Playwright

```bash
playwright install
```

---

### 5. Subir Redis

Opção com Docker:

```bash
docker run -d -p 6379:6379 redis
```

---

### 6. Rodar backend

```bash
uvicorn app.main:app --reload
```

---

### 7. Rodar worker

```bash
celery -A worker.worker worker --loglevel=info
```

---

## 🧪 Exemplo de Endpoint

### Disparar automação

```http
POST /automation/run
```

Body:

```json
{
  "task_name": "example_rpa"
}
```

---

## 🤖 Exemplo de Automação (Playwright)

```python
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://example.com")
        title = page.title()

        browser.close()
        return title
```

---

## ⚠️ Considerações importantes

### 🔒 Segurança

* Nunca armazene credenciais em texto plano
* Utilize variáveis de ambiente
* Proteja endpoints com autenticação

---

### 👥 Multiusuário

* Use contextos isolados no Playwright
* Evite compartilhar sessões entre usuários

---

### ⚡ Escalabilidade

* Execuções simultâneas podem sobrecarregar o servidor
* Considere limitar concorrência

---

### 🌐 Acesso externo

Para expor sua API:

* Configure port forwarding no roteador
* Ou utilize **Ngrok**

---

## 📈 Melhorias futuras

* Dashboard com status das execuções
* Histórico de tarefas
* Upload de scripts RPA
* Autenticação JWT
* Deploy em cloud (AWS, GCP, etc.)
* Orquestração com Docker Compose

---

## 🧭 Roadmap

* [ ] MVP funcional
* [ ] Sistema de autenticação
* [ ] Controle de fila
* [ ] Execução paralela
* [ ] Interface web (React ou similar)
* [ ] Deploy em produção

---

## 💡 Objetivo do projeto

Este projeto serve como:

* Estudo de arquitetura backend
* Introdução a filas e processamento assíncrono
* Uso prático de automação com Playwright
* Base para construção de um SaaS de RPA

---

## 🧑‍💻 Autor

Desenvolvido como projeto de estudo para evolução em backend, automação e engenharia de dados.

---
