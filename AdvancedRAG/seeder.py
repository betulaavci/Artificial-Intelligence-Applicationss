from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Çevre değişkenlerini yükleyin
load_dotenv()

# Web sayfalarının URL listesi
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

# URL'lerden belgeleri yükleyin
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

# Metinleri parçalara bölmek için bir metin bölücü oluşturun
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

# Belgeleri parçalara bölün
splits = text_splitter.split_documents(docs_list)

# OpenAI Embeddings ile gömme işlevi oluşturun
embedding_function = OpenAIEmbeddings()

# Chroma vektör deposunu oluşturun
vector_store = Chroma.from_documents(
    documents=splits,
    collection_name="rag-chroma",
    embedding=embedding_function,
    persist_directory="./.chroma"
)

# Chroma vektör deposundan bir retriever (alıcısı) oluşturun, `embedding` parametresi olmadan
retriever = vector_store.as_retriever()
