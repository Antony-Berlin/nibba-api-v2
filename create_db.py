import os
import chromadb
from chromadb.config import Settings
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter


# Define the folder path containing the text documents
folder_path = "data/collection1"
client = chromadb.PersistentClient(path="vector_DB",settings=Settings(allow_reset=True, anonymized_telemetry=False))

client.heartbeat() 
client.reset() 
collection_1 = client.create_collection(
        name = "collection_1",
        metadata = {"hnsw:space": "cosine"}, # l2 is the default
        get_or_create = True
    )
# List to store all documents
all_documents = []
indices = []

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):  # Assuming all files are text files
        file_path = os.path.join(folder_path, filename)
        print(filename+"\n")
        # Load the text from the file
        loader = TextLoader(file_path)
        documents = loader.load()
        # documents = [str(doc) for doc in documents]
        # Add the documents to the list
        all_documents.extend(documents)
        

# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(all_documents)

data =[]
metadata = []
for doc in docs:
    data.append(doc.page_content)
    metadata.append(doc.metadata)
print(len(docs))
indices = [str(i) for i in range(1, len(docs)+1)]


# Load it into Chroma
collection_1.upsert(
    documents=data,
    metadatas=metadata,
    ids=indices
)
