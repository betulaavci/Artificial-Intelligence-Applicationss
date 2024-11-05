from dotenv import load_dotenv
load_dotenv()
from graph.graphh import app


if __name__ == "__main__":
    print("Hello Advanced RAG")
    print(app.invoke(input={"question": "How to make hamburgers"}))


