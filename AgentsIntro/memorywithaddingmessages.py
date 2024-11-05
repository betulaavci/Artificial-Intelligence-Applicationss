from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import OpenAI


load_dotenv()

memory = []


search = TavilySearchResults(max_results=1)
tools = [search]

prompt = hub.pull("hwchase17/react-chat")


llm = OpenAI()

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
config = {"configurable": {"thread_id": "abc123"}}

if __name__ == '__main__':
    chat_history = []

    while True:
        user_input = input(">")

        memory.append(f"Human: {user_input}")

        response = []

        for chunk in agent_executor.stream(
                {
                    "input": user_input,
                    "chat_history": "\n".join(memory),
                },
                config
        ):
            if 'text' in chunk:
                print(chunk['text'], end='')
                response.append(chunk['text'])

        memory.append(f"AI: {''.join(response)}")
        print("\n----")
