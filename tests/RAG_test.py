import os
from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone import Pinecone
import openai
import time

def generate_response(user_query):
    load_dotenv()
    try:
        os.environ["HF_TOKEN"] = os.environ.get("HF_TOKEN")

        embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")

        bm25_encoder = BM25Encoder().default()

        index_name = "hybrid-search-langchain-pinecone"

        pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))

        index = pc.Index(index_name)

        retriever = PineconeHybridSearchRetriever(embeddings=embeddings, sparse_encoder=bm25_encoder, index=index)

        context = retriever.invoke(user_query)

        import openai

        # Set up your API key
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        message = f'''You are a personal fitness trainer that answers clients' questions about fitness and diet related topics.
        Use the provided context to answer the question. If the context is not useful, generate a response based on your previous knowledge.
        The user question is {user_query}. The context is: {context}
                    '''
        # Call the OpenAI API with streaming
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or 'gpt-3.5-turbo'
            messages=[{"role": "user", "content": message}],
            max_tokens=150,  # You can adjust this
            stream=True  # Enable streaming mode
        )
        time.sleep(10)
        # Print each token as it arrives
        print("Assistant response:", end=" ", flush=True)
        for chunk in response:
            if 'choices' in chunk:
                delta_content = chunk['choices'][0]['delta'].get('content', '')
                print(delta_content, end="", flush=True)

        return response
    except:
        return "There was an error generating your response"

if __name__ == '__main__':   
    generate_response("I am starting working out and need bodyweight exercises to gain upper chest strength. Any reccomendations?")