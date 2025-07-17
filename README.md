#  Hotmart AI Support

Sistema de atendimento inteligente com agentes especializados e busca em base de conhecimento usando RAG com Qdrant.  
Projetado para responder dúvidas de clientes sobre programas como *Hotmart Journey Stars* e *Legacy*, de forma automática, contextual e precisa.

---
## Relatório

📄 [relatorio_hotmart_ai_support.pdf](./relatorio_hotmart_ai_support.pdf)
---

##  Funcionalidades

- **Agente Multi-Especializado**: pipeline de agentes (LangGraph) para lidar com diferentes tópicos (Journey, FAQ).
- **RAG com Qdrant**: busca por similaridade usando embeddings e recuperação de contexto relevante.
- **API FastAPI**: interface REST para interação com o sistema.
- **Mock de Dados Financeiros**: simulação de faturas e informações de clientes.
- **Indexação Automatizada**: indexa a base de conhecimento automaticamente ao iniciar o container.

---

## ▶ Como Rodar o Projeto

###  Opção 1: Com Docker (recomendado para produção e testes rápidos)

Não é necessário instalar **Poetry** nem gerenciar dependências manualmente. Basta rodar:

```bash
git clone <url-do-repositório>
cd hotmart-ai-support
docker compose up -d --build
```

A aplicação estará disponível em:

- API: [http://localhost:8000](http://localhost:8000)  
- Qdrant Dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

> ! A base de conhecimento será indexada automaticamente no primeiro build.

---

###  Opção 2: Ambiente Local com Poetry (para desenvolvimento)

#### 1. Pré-requisitos

- Python 3.12
- [Poetry](https://python-poetry.org/docs/#installation)

#### 2. Instalação

```bash
git clone <url-do-repositório>
cd hotmart-ai-support
poetry install
```

#### 3. Rodar a API localmente

```bash
poetry run uvicorn src.api.main:app --reload
```

#### 4. Indexar manualmente (se necessário)

```bash
poetry run python -m scripts.indexer
```

---

##  Arquitetura dos Agentes (LangGraph)

Abaixo está o fluxo dos agentes do sistema de atendimento inteligente, implementado com LangGraph:

![Fluxo de Agentes](src/ai_engine/graph_visualization/chat_flow.png)

---

### Descrição dos Agentes

| Agente                | Descrição |
|----------------------|-----------|
| **Guardrail**        | Verifica se a mensagem do usuário é apropriada e decide se o atendimento continua ou é encerrado. Atua como camada de segurança inicial. |
| **Router**           | Classifica a intenção da pergunta e direciona para o agente apropriado: `faq`, `journey` ou `atendente` humano. |
| **FAQ Agent**        | Utiliza RAG para responder perguntas frequentes sobre produtos, serviços e termos da Hotmart. |
| **Journey Agent**    | Especialista em dúvidas sobre os programas *Hotmart Journey Stars* e *Legacy*. Usa informações da base em prompt + dados financeiros personalizados. |
| **Customer Service** | Mensagem final do atendente para o usuário quando há a necessidade de atendimento. |


---

##  Estrutura do Projeto

```bash
.
├── src/                   # Código principal da aplicação
│   ├── api/              # FastAPI (rotas, serviços, modelos)
│   ├── ai_engine/        # Agentes LangGraph
│   ├── rag/              # Indexação e recuperação com Qdrant
│   ├── tools/            # Ferramentas auxiliares
│   └── config.py         # Configurações globais
├── scripts/              # Scripts de indexação e visualização
├── examples/             # Exemplos de entrada cURL
├── hormart_dataset.csv   # Base de conhecimento (FAQ / Journey)
├── Dockerfile            # Container da aplicação
├── docker-compose.yml    # Orquestração dos containers
├── pyproject.toml        # Dependências com Poetry
├── .env.example          # Variáveis de ambiente
└── README.md             # Este arquivo :)
```

---

##  Configuração `.env`

Crie um arquivo `.env` na raiz com o seguinte conteúdo:

```env
# Qdrant configuration
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# OpenAI configuration
OPENAI_API_KEY=your-openai-api-key

# Qdrant collection name
COLLECTION_NAME=hotmart
```

>  Se estiver rodando localmente fora do Docker, altere `QDRANT_HOST` para `localhost`.

---

##  Modelo LLM Utilizado

Modelo padrão: `gpt-4o-mini` da OpenAI.

Vantagens:

- Alta velocidade de inferência
- Custo reduzido

>  Para usar outro modelo (ex: `gpt-3.5-turbo`, `gpt-4o`), basta alterar nas definições dos agentes.

---

##  RAG Híbrido com Vetores e BM25

Combinação de:

- **Vetores densos**: `text-embedding-3-small` (OpenAI)
- **Vetores esparsos**: `Qdrant/bm25` (open-source)

### Funcionamento:

1. A pergunta do usuário é convertida em vetores densos e esparsos.
2. O Qdrant calcula a similaridade em ambas as representações.
3. Os documentos mais relevantes são retornados, mesmo com linguagem variada.

>  Ideal para FAQs e artigos curtos com vocabulário fixo.

---

##  Mock de Dados Financeiros

Simulação de faturas dos usuários com base no `user_id` para respostas personalizadas sobre o Hotmart Journey.

- Fonte: `src/data/mock_billing_data.json`
- Dados carregados automaticamente durante a execução do agente

---

##  API - Exemplo de Uso

### Endpoint

```http
POST /chat
```

### Requisição

```json
{
  "user_id": 123,
  "question": "Quais os benefícios eu tenho no Programa Hotmart Journey?"
}
```

### Resposta (exemplo)

```json
{
  "answer": "Olá, Maria! Com base nas suas informações, aqui estão os benefícios que você pode ter no Programa Hotmart Journey:\n\n### Hotmart Journey Stars\n- **Performance nos últimos 12 meses**: Você alcançou R$ 125.000,00 em faturamento líquido...\n\n### Hotmart Journey Legacy\nVocê está no **Hotmart Mission** do **Earth Chapter**...\n\n**Recompensas**: ...\n\n### Cartão Hotmart\nVocê pode solicitar o **Cartão Hotmart** na categoria **Business**...",
  "agent_name": "faq_agent_node",
  "timestamp": "2025-07-17T04:18:14.546477",
  "chat_id": "f09eb87a-7e63-4514-b29e-01abf6f3a90c",
  "sources": []
}
```

---

##  Base de Conhecimento

- Fonte: `hormart_dataset.csv`
- Campos esperados: `article_name`, `article_url`, `article_content`
- Indexação automática ao iniciar o container


---

##  Autoria

Desenvolvido por [@evellynnicole](https://github.com/evellynnicole)
