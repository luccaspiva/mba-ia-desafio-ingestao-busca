import os
from dotenv import load_dotenv
from search import search_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def main():
    print("Chatbot iniciado! Digite 'sair' para encerrar.")
    print("=" * 50)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    chain = search_prompt() | llm

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    while True:
        user_input = input("\nPERGUNTA: ")
        if user_input.lower() in ['sair', 'exit', 'quit']:
            print("Encerrando o chat. Até logo!")
            break

        response = chain.invoke(user_input)
        print(f"\nRESPOSTA: {response.content}")

if __name__ == "__main__":
    main()