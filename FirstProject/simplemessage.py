from dotenv import load_dotenv, dotenv_values
from langchain_openai import ChatOpenAI
load_dotenv()
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
"""messages = [
    SystemMessage(content="Translate the following from English to Spanish"),
    HumanMessage(content="Hi!"),
]"""
system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

parser = StrOutputParser()
chain = prompt_template | model | parser

if __name__ =="__main__":
    print(chain.invoke({"language": "italian", "text": "hi"}))
