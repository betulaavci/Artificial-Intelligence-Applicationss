from dotenv import load_dotenv, dotenv_values

load_dotenv()

API_KEY = dotenv_values(".env").get("OPENAI_API_KEY")
print(API_KEY)