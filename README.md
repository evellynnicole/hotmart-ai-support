#  Hotmart AI Support

Sistema de atendimento inteligente com agentes especializados e busca em base de conhecimento usando RAG com Qdrant.  
Projetado para responder dúvidas de clientes sobre programas como *Hotmart Journey Stars* e *Legacy*, de forma automática, contextual e precisa.

---

##  Funcionalidades

-  **Agente Multi-Especializado**: pipeline de agentes (LangGraph) para lidar com diferentes tópicos (Journey, FAQ, Billing).
-  **RAG com Qdrant**: busca por similaridade usando embeddings e recuperação de contexto relevante.
-  **API FastAPI**: interface REST para interação com o sistema.
-  **Mock de Dados Financeiros**: simulação de faturas e informações de clientes.
-  **Indexação Automatizada**: indexa base de conhecimento automaticamente ao iniciar o container.

---

##  Como Rodar

### 1. Pré-requisitos

- Python 3.12
- Docker e Docker Compose
- Poetry

### 2. Instalação Local

```bash
git clone <url>

cd hotmart-ai-support

poetry install
```

### 3. Rodando com Docker

```bash
docker compose up -d --build
```

- Aplicação: [http://localhost:8000](http://localhost:8000)  
- Dashboard Qdrant: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## 📁 Estrutura do Projeto

```bash
.
├── src/                   # Código principal da aplicação
│   ├── api/              # FastAPI (rotas, serviços, modelos)
│   ├── ai_engine/        # Agentes LangGraph
│   ├── rag/              # Indexação e recuperação com Qdrant
│   ├── tools/            # Ferramentas auxiliares
│   └── config.py         # Configurações globais
├── scripts/              # Scripts de indexação e visualização
├── hormart_dataset.csv   # Base de conhecimento (FAQ / Journey)
├── Dockerfile            # Container da aplicação
├── docker-compose.yml    # Orquestração dos containers
├── pyproject.toml        # Dependências com Poetry
├── .env.example          # Variáveis de ambiente
└── README.md             # Este arquivo :)
```
---

## Configuração via `.env`

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

> 🔧 A variável `QDRANT_HOST=qdrant` assume que você está usando Docker. Se rodar localmente sem container, altere para `localhost`.

---

##  Modelo LLM Utilizado (OpenAI)

Usei o modelo `gpt-4o-mini` da OpenAI, ideal para aplicações em produção por oferecer:

-  Alta velocidade de inferência
-  Custo reduzido comparado a outros modelos

> Se quiser trocar para outro modelo (ex: `gpt-3.5-turbo`, `gpt-4`), basta ajustar nas classes dos agentes.

---

## Vetores e Recuperação Híbrida com `Qdrant/bm25`

Este projeto usa RAG híbrido, combinando:

- **Vetores densos** com embeddings da OpenAI (`text-embedding-3-small`)
- **Vetores esparsos** com BM25 (`Qdrant/bm25`) - Modelo Open Source

A configuração é feita via:

```python
sparse_model = 'Qdrant/bm25'
```

### Como funciona:

1. A pergunta do usuário é embutida tanto com vetores densos quanto esparsos.
2. O Qdrant calcula similaridade com base em ambos os formatos.
3. O sistema retorna os documentos mais relevantes, mesmo com variações na linguagem.

Essa abordagem melhora significativamente a **precisão em FAQs e artigos curtos** com linguagem fixa.

---

## Dados Mockados de Faturamento

O sistema simula informações reais de faturamento dos usuários para fornecer respostas personalizadas nos programas **Hotmart Journey Stars** e **Legacy**.

Esses dados são carregados automaticamente durante a execução do agente e usados para enriquecer a resposta com base no `user_id` informado.

### 📄 Arquivo de origem:

`src/data/mock_billing_data.json`

---

##  API - Exemplo de Uso

### Endpoint

```http
POST /chat
```

### Body

```json
{
  "user_id": 123,
  "question": "Quais os benefícios eu tenho no Programa Hotmart Journey?"
}
```

### Response (exemplo)

```json
{
  "answer": "Olá, Maria! Com base nas suas informações, aqui estão os benefícios que você pode ter no Programa Hotmart Journey:\n\n### Hotmart Journey Stars\n- **Performance nos últimos 12 meses**: Você alcançou R$ 125.000,00 em faturamento líquido nos últimos 12 meses, o que pode lhe proporcionar encontros e experiências memoráveis como parte das recompensas da trilha de performance.\n\n### Hotmart Journey Legacy\nVocê está no **Hotmart Mission** do **Earth Chapter**, pois seu faturamento líquido total acumulado é de R$ 560.000,00. Aqui estão os marcos que você já atingiu:\n\n- **Hotmart Project**: Cadastro de produto.\n- **Hotmart Blueprint**: R$ 10 mil em faturamento líquido.\n- **Hotmart Build**: R$ 100 mil em faturamento líquido.\n- **Hotmart Spaceship**: R$ 250 mil em faturamento líquido.\n- **Hotmart Mission**: R$ 500 mil em faturamento líquido.\n\n**Recompensas**: Você já deve ter recebido badges na sua wallet e pode ter recebido um quadro comemorativo.\n\n### Cartão Hotmart\n- Você pode solicitar o **Cartão Hotmart** na categoria **Business**, que oferece benefícios exclusivos para ajudar a investir no seu negócio com mais segurança.\n\nSe precisar de mais informações ou ajuda para solicitar suas recompensas, você pode entrar em contato com a [Central de Ajuda](https://help.hotmart.com).\n\nSe tiver mais dúvidas ou precisar de assistência adicional, estou à disposição!",
  "agent_name": "faq_agent_node",
  "timestamp": "2025-07-17T04:18:14.546477",
  "chat_id": "f09eb87a-7e63-4514-b29e-01abf6f3a90c",
  "sources": []
}
```

---

##  Base de Conhecimento

- Arquivo: `hormart_dataset.csv`
- Indexado automaticamente ao iniciar.
- Campos esperados: `article_name`, `article_url`,  `article_content`, 

---

##  Testes Locais

Para indexar manualmente os documentos:

```bash
poetry run python -m scripts.indexer
```

---

##  Autoria

Desenvolvido por [@evenicole](https://github.com/evenicole).