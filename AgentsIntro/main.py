from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import sqlite3

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS memory_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT
    )
''')
conn.commit()

def save_message_to_memory(message):
    cursor.execute('INSERT INTO memory_records (message) VALUES (?)', (message,))
    conn.commit()

def get_all_messages_from_memory():
    cursor.execute('SELECT * FROM memory_records')
    return cursor.fetchall()

search = TavilySearchResults(max_results=2)
tools = [search]

agent_executor = create_react_agent(model, tools)

config = {"configurable": {"thread_id": "abc123"}}

if __name__ == "__main__":
    while True:
        user_input = input(">")
        save_message_to_memory(user_input)

        for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
        ):
            print(chunk)
            print("----")

        print("Bellekteki tüm mesajlar:")
        all_messages = get_all_messages_from_memory()
        for msg in all_messages:
            print(msg)

