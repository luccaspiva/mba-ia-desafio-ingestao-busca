from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv

from ingest import store

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_context(query):
    """Função que busca no banco e retorna o contexto formatado"""
    results = store.similarity_search_with_score(query, k=10)
    
    if not results:
        return "Não encontrei informações relevantes no contexto fornecido."

    context = "\n\n".join([doc.page_content.strip() for doc, _ in results])
    return context

def search_prompt():
    """Retorna uma chain do LangChain"""
    
    retriever = RunnableLambda(search_context)
    
    prompt = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )
    
    chain = (
        {
            "contexto": retriever,
            "pergunta": RunnablePassthrough()
        }
        | prompt
    )
    
    return chain