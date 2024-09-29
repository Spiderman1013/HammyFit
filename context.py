from dotenv import load_dotenv
from langchain_community.retrievers import PineconeHybridSearchRetriever
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder
from load_dataset import chunk_pdf_text
load_dotenv()

sentences = chunk_pdf_text('exercisebook.pdf')

index_name = "hybrid-search-langchain-pinecone"

pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name = index_name,
        dimension = 384,
        metric = "dotproduct",
        spec = ServerlessSpec(cloud = "aws", region = "us-east-1")
    )

index = pc.Index(index_name)

#huggingfacetoken need to add
os.environ["HF_TOKEN"] = os.environ.get("HF_TOKEN")

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")

bm25_encoder = BM25Encoder().default()


#bm25_encoder.fit(sentences)

#bm25_encoder.dump("values.json")

#bm25_encoder = BM25Encoder().load("values.json")

#adding  exercise book to pinecone

retriever = PineconeHybridSearchRetriever(embeddings=embeddings, sparse_encoder=bm25_encoder, index=index)

retriever.add_texts(sentences)

#Querying
user_query = "What are the best exercises to grow my upper chest?"

results = retriever.invoke(user_query)

# Print the results
for result in results:
    print(result)
