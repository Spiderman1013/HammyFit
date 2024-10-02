import os
import time
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone import Pinecone
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Set API keys
os.environ["HF_TOKEN"] = os.environ.get("HF_TOKEN")
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# Disable tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def setup_embeddings_and_retriever(index_name):
    """Set up embeddings and Pinecone retriever."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    bm25_encoder = BM25Encoder().default()
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index = pc.Index(index_name)
    retriever = PineconeHybridSearchRetriever(embeddings=embeddings, sparse_encoder=bm25_encoder, index=index)
    return retriever

def generate_chat_response(user_query, context):
    """Generate a response using LangChain's updated ChatOpenAI."""
    # Initialize ChatOpenAI with the API key from the environment
    llm = ChatOpenAI(model="gpt-4o-mini")  # or 'gpt-3.5-turbo'
    print(context)
    # Create a structured message for the model
    messages = [
        {"role": "user", "content": f'''
         You are a personal fitness trainer that answers clients' questions about fitness and diet-related topics.
        Use the provided context to answer the question. If the context is not useful, generate a response based on your previous knowledge. Please state if you used the context at the beginning of the response and cite what you used. 
        Please format all text without any markup modifications.
        The user question is: "{user_query}". The context is: {context}''' }
    ]

    # Use the invoke method instead of __call__
    response = llm.invoke(messages)

    # Access the response correctly based on the latest structure
    return response.content if hasattr(response, 'content') else response['choices'][0]['message']['content']

def generate_response(user_query):
    """Main function to generate response for a user's query."""
    try:
        index_name = "hybrid-search-langchain-pinecone"
        retriever = setup_embeddings_and_retriever(index_name)

        context = retriever.invoke(user_query)
        response = generate_chat_response(user_query, context)

        print("Assistant response:", response)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "There was an error generating your response."

def retrieve_context(user_query):
    """Main function to generate response for a user's query."""
    try:
        index_name = "hybrid-search-langchain-pinecone"
        retriever = setup_embeddings_and_retriever(index_name)

        context = retriever.invoke(user_query)
        return context
    except Exception as e:
        print(f"Error: {e}")
        return "There was an error generating your response."


# Example usage
#generate_response("I am starting to work out and need bodyweight exercises to gain upper chest strength. Any recommendations?")
