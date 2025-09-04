from langchain_openai import ChatOpenAI

from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()
 

llm = ChatOpenAI(model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))

 

def analyze_email(subject: str, body: str) -> str:

    messages = [

        SystemMessage(content="Du är en hjälpsam e-postassistent."),

        HumanMessage(content=f"Mejl ämne: {subject}\nMejl text: {body}\n\nSka vi svara på detta mejl? Om ja, skriv ett svar, annars skriv 'Ignorera'.")

    ]

    response = llm.invoke(messages)

    return response.content