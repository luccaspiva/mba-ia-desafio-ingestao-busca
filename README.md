# Desafio MBA IA - Sistema de Ingestão e Busca em PDF

Sistema de RAG (Retrieval-Augmented Generation) que permite fazer perguntas sobre o conteúdo de um PDF usando LangChain, PostgreSQL com pgVector e Google Gemini.

## 🎯 Objetivo

Criar um software capaz de:

- **Ingestão**: Ler um arquivo PDF e salvar suas informações em um banco PostgreSQL com extensão pgVector
- **Busca**: Permitir perguntas via CLI e receber respostas baseadas apenas no conteúdo do PDF

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.11+
- **Framework**: LangChain
- **Banco de dados**: PostgreSQL + pgVector
- **Containerização**: Docker & Docker Compose
- **LLM**: Google Gemini (gemini-1.5-flash)
- **Embeddings**: Google Generative AI Embeddings (models/embedding-001)

## 📁 Estrutura do Projeto

```
├── docker-compose.yml      # Configuração do PostgreSQL com pgVector
├── requirements.txt        # Dependências Python
├── .env                   # Variáveis de ambiente
├── document.pdf           # PDF para ingestão
├── src/
│   ├── ingest.py          # Script de ingestão do PDF
│   ├── search.py          # Sistema de busca e retrieval
│   └── chat.py            # Interface CLI para interação
└── README.md
```

## ⚙️ Configuração

### 1. Pré-requisitos

- Clonar projeto
- Python 3.11 ou superior
- Docker e Docker Compose
- API Key do Google Gemini

### 2. Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto, baseando-se no arquivo `.env.example`:

```env
GOOGLE_API_KEY=<your_google_api_key>
GOOGLE_EMBEDDING_MODEL=models/embedding-001
PGVECTOR_URL=postgresql://user:password@localhost:5432/mydatabase
PGVECTOR_COLLECTION=gpt5_collection
PDF_PATH=./document.pdf
```

### 5. Adicionar PDF

Coloque seu arquivo PDF na raiz do projeto com o nome `document.pdf` ou ajuste o caminho no `.env`.

## 🚀 Como Executar

### 1. Iniciar o Banco de Dados

```bash
docker-compose up -d
```

Verifique se está rodando:
```bash
docker ps
```

### 2. Fazer Ingestão do PDF

```bash
python src/ingest.py
```

Este comando vai:
- Carregar o PDF
- Dividir em chunks de 1000 caracteres (overlap de 150)
- Converter em embeddings
- Armazenar no PostgreSQL

### 3. Iniciar o Chat

```bash
python src/chat.py
```

## 💬 Exemplo de Uso

```
Chatbot iniciado! Digite 'sair' para encerrar.
==================================================

PERGUNTA: Qual o faturamento da empresa XPTO?
RESPOSTA: O faturamento da empresa foi de 10 milhões de reais.

PERGUNTA: Quando foi fundada a empresa XPTO?
RESPOSTA: 2018.

PERGUNTA: Quantos funcionários trabalham na empresa?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

PERGUNTA: Qual a capital do Brasil?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

PERGUNTA: sair
Encerrando o chat. Até logo!
```

## 🔧 Arquitetura Técnica

### Sistema de Ingestão (`ingest.py`)
- Carrega PDF usando `PyPDFLoader`
- Divide texto com `RecursiveCharacterTextSplitter`
- Gera embeddings com Google Generative AI
- Armazena no PostgreSQL com pgVector

### Sistema de Busca (`search.py`)
- Implementa busca por similaridade usando `similarity_search_with_score`
- Cria chain do LangChain para processamento
- Formata prompt com contexto recuperado
- Retorna apenas informações do PDF

### Interface de Chat (`chat.py`)
- CLI interativo para perguntas do usuário
- Integração com chain de busca
- Respostas via Google Gemini
- Tratamento de erros e comandos de saída

## 🎯 Regras do Sistema

O sistema segue regras rígidas:

- ✅ **Responde APENAS com base no PDF**
- ❌ **Nunca inventa informações**
- ❌ **Não usa conhecimento externo**
- ❌ **Não produz opiniões**

Para perguntas fora do contexto, sempre responde:
> "Não tenho informações necessárias para responder sua pergunta."

## 📋 Dependências Principais

```
langchain==0.2.16
langchain-google-genai==1.0.8
langchain-community==0.2.16
langchain-postgres==0.0.12
python-dotenv==1.0.1
psycopg2-binary==2.9.9
pypdf==4.3.1
```

## 🐛 Troubleshooting

### Erro de conexão com banco
```bash
# Verificar se o container está rodando
docker-compose ps

# Reiniciar o banco
docker-compose down
docker-compose up -d
```

### Erro de API Key
- Verifique se a `GOOGLE_API_KEY` está configurada no `.env`
- Confirme se a API Key é válida no Google AI Studio

### PDF não encontrado
- Verifique o caminho no `PDF_PATH` do `.env`
- Confirme se o arquivo existe no local especificado

## 📚 Links Úteis

- [LangChain Documentation](https://python.langchain.com/)
- [Google AI Studio](https://makersuite.google.com/)
- [pgVector Documentation](https://github.com/pgvector/pgvector)

---

**Desenvolvido como parte do MBA em Engenharia de Software com IA - Full Cycle**