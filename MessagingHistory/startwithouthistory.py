from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

#print(model.invoke([HumanMessage(content="Hello, my name is Betül")]))
#print(model.invoke([HumanMessage(content="What's my name?")]))


if __name__ == "__main__":
    response = model.invoke(
        [
            HumanMessage(content="Hi! I'm Betül"),
            AIMessage(content="Hello Betül! How can I assist you today?"),
            HumanMessage(content="What's my name?"),
        ]
    )
    print(response.content)