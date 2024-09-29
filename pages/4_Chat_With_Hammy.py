import streamlit as st
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from query2 import retrieve_context
from exerciseapi import get_exercise_image, get_exercise_video
from dotenv import load_dotenv
import os
import re
from setPage import set_up_page
set_up_page()

def remove_links(text):
    # This regex pattern matches URLs
    pattern = r'https?://\S+|www\.\S+'
    return re.sub(pattern, '', text)

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
st.title("💬 Chat with Hammy!")



# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "avatar": 'hammy_gifs/working_hammy.gif', "content": "Hey, I'm Hammy! Tell me any fitness question!"}]
if "prompt_counter" not in st.session_state:
    st.session_state["prompt_counter"] = 0

# Function to clear the chat history
def clear_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hey, I'm Hammy! Tell me any fitness question!"}]
    st.session_state.prompt_counter = 0  # Reset the counter

# Add a clear history button
if st.button("Clear History"):
    clear_history()

# Display messages in chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"], avatar='hammy_gifs/working_hammy.gif' if msg['role'] is 'assistant' else 'hammy_gifs/user-24.png').write(msg["content"])

# Initialize LangChain components
memory = ConversationBufferMemory(memory_key="chat_history")
llm = OpenAI(name='gpt-3.5-turbo', api_key=openai_api_key)

# Initialize the tools for the agent
tools = [
    Tool(name="Textbook Knowledge", func=retrieve_context, description="Retrieve textbook knowledge about fitness."),
]

agent = initialize_agent(tools, llm, memory=memory, agent_type="REACT_DOCSTORE", verbose=True, handle_parsing_error=True)

if prompt := st.chat_input():
    # Update session state with user prompt
    st.session_state.messages.append({"role": "user", "avatar": 'hammy_gifs/user-24.png', "content": prompt})
    st.chat_message("user").write(prompt)

    # Increment the prompt counter
    st.session_state.prompt_counter += 1

    # Clear history if the counter reaches 3
    if st.session_state.prompt_counter >= 3:
        memory = ConversationBufferMemory(memory_key="chat_history")  # Reset memory

    # Create the prompt for the LangChain agent
    langchain_prompt = f'''
    You are a knowledgeable and friendly personal fitness trainer. Your task is to answer the users about fitness topics. 
    Use your tools effectively and methodically to assist the client. If none of the tools work, use your prior knowledge. 
    You may only make one observation. After that, you must formulate an answer.
    Please give an in-depth answer of at least 2 paragraphs. 

    The user's question is: "{prompt}"
    '''

    # Show a spinner while waiting for the response
    with st.spinner("Hammy is thinking..."):
        thinking = st.image('hammy_gifs/thinking_hammy.gif')
        # Get response from the LangChain agent
        response = agent.run(langchain_prompt)

        thinking.empty()


    st.session_state.messages.append({"role": "assistant", "content": response})    
    st.chat_message("assistant", avatar='hammy_gifs/working_hammy.gif').write(response)
