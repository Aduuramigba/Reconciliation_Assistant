from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
import re
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

text_loader_kwargs = {"encoding": "utf-8"}

loader = DirectoryLoader(
    path="data",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs=text_loader_kwargs
)
folder_docs = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(folder_docs)

# Extract image paths
for chunk in chunks:
    image_paths = re.findall(r'!\[.*?\]\((.*?)\)', chunk.page_content)
    chunk.metadata["images"] = ",".join(image_paths)

embeddings = OpenAIEmbeddings()

db_name = "chroma_db"

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=db_name
)

vectorstore.persist()
print("✅ Knowledge base ingested and saved!")
