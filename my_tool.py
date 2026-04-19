from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv


load_dotenv(override=True)

embeddings = OpenAIEmbeddings()
db_name = "chroma_db"
vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o-mini")
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

retriever = vectorstore.as_retriever()
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

print("✅ Vectorstore loaded, ready for queries!")

