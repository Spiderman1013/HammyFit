import streamlit as st
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
#from helpers.exerciseapi import get_exercise_image, get_exercise_video
from dotenv import load_dotenv
import re
from helpers.setPage import set_up_page
set_up_page()


import os
import sys
original_sys_path = sys.path.copy()
# Navigate to the grandparent directory

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))  # Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(parent_dir, '..'))  # Get the absolute path of the parent directory
sys.path.append(parent_dir)  # Add the grandparent directory to the system path
from helpers.RAG import retrieve_context

sys.path = original_sys_path.copy()  # Reset the system path

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))  # Get the absolute path of the parent directory
hammy_gifs_path = os.path.join(parent_dir, 'assets', 'hammy_gifs')
print(hammy_gifs_path)


def remove_links(text):
    # This regex pattern matches URLs
    pattern = r'https?://\S+|www\.\S+'
    return re.sub(pattern, '', text)

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
st.title("💬 Chat with Hammy!")



# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "avatar": f'{hammy_gifs_path}/working_hammy.gif', "content": "Hey, I'm Hammy! Tell me any fitness question!"}]
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
    st.chat_message(msg["role"], avatar=f'{hammy_gifs_path}/working_hammy.gif' if msg['role'] is 'assistant' else f'{hammy_gifs_path}/user-24.png').write(msg["content"])

# Initialize LangChain components
memory = ConversationBufferMemory(memory_key="chat_history")
llm = OpenAI(name='gpt-3.5-turbo', api_key=openai_api_key)

# Initialize the tools for the agent
tools = [
    Tool(name="Textbook Knowledge", func=retrieve_context, description="Use this tool for complex or technical fitness questions that require in-depth, textbook knowledge."),
]

agent = initialize_agent(tools, llm, memory=memory, agent_type="REACT_DOCSTORE", verbose=True, handle_parsing_errors=True)

if prompt := st.chat_input():
    # Update session state with user prompt
    st.session_state.messages.append({"role": "user", "avatar": f'{hammy_gifs_path}/user-24.png', "content": prompt})
    st.chat_message("user", avatar=f'{hammy_gifs_path}/user-24.png').write(prompt)

    # Increment the prompt counter
    st.session_state.prompt_counter += 1

    # Clear history if the counter reaches 3
    if st.session_state.prompt_counter >= 3:
        memory = ConversationBufferMemory(memory_key="chat_history")  # Reset memory

    # Create the prompt for the LangChain agent
    langchain_prompt = f'''
    You are a knowledgeable and friendly personal fitness trainer named Hammy. Your task is to answer users about fitness topics. 
    Only use the "Textbook Knowledge" tool if the user's question seems highly technical or involves complex information. 
    If the question does not require the use of any tools, simply provide an answer using your prior knowledge.
    The user's question is: "{prompt}"
    '''

    # Show a spinner while waiting for the response
    with st.spinner("Hammy is thinking..."):
        thinking = st.image(f'{hammy_gifs_path}/thinking_hammy.gif')
        # Get response from the LangChain agent
        response = agent.run(langchain_prompt)

        thinking.empty()


    st.session_state.messages.append({"role": "assistant", "content": response})    
    st.chat_message("assistant", avatar=f'{hammy_gifs_path}/working_hammy.gif').write(response)
