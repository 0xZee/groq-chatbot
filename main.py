import streamlit as st
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core.chat_engine import SimpleChatEngine

# page config
st.set_page_config(page_title="Groq ChatBot", page_icon=":robot_face:",
                   layout="centered", initial_sidebar_state="auto", menu_items=None)

# sidebar
with st.sidebar:
    st.code("OxZee Groq Inference ChatBot")
    st.code("https://github.com/0xZee/groq-chatbot/")
    st.subheader("GROQ API", divider="grey")
    if ("GROQ_API" in st.secrets and st.secrets['GROQ_API'].startswith('gsk_')):
        st.success('Your GROQ API key is provided')
        api_key = st.secrets['GROQ_API']
    else:
        api_key = st.text_input('Enter your Groq API Key', type='password')
        if not (api_key.startswith('gsk_') and len(api_key) == 56):
            st.warning("Enter a Valid GROQ API key")
        else:
            st.success('GROQ API Key Provided')

    st.subheader("MODEL", divider="grey")
    user_model = st.selectbox(
        "Select Model", ["llama3-8b-8192", "gemma-7b-it", "mixtral-8x7b-32768"])

    st.divider()
    if st.button("Clear Chat Session", use_container_width=True, type="secondary"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm here to help, Ask me a question ! :star:"}]


# main page
with st.container(border=True):
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader(
            "💬 :orange-background[GROQ] :orange[CHATBOT] ", divider='orange')
    with c2:
        if user_model == "llama3-8b-8192":
            st.subheader(f"🤖 :orange-background[LLAMA3]", divider='orange')
        if user_model == "gemma-7b-it":
            st.subheader(f"🤖 :orange-background[GEMMA]", divider='orange')
        if user_model == "mixtral-8x7b-32768":
            st.subheader(f"🤖 :orange-background[MISTRAL]", divider='orange')

# function
# Setting LLM
model_llama = "llama3-8b-8192"
model_gemma = "gemma-7b-it"
model_mixtral = "mixtral-8x7b-32768"
model_whistper = "whisper-large-v3"

LLM_GROQ = Groq(model=user_model, api_key=api_key)
Settings.llm = LLM_GROQ


# fuctions
#
# Initialize the chat messages history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm here to help, Ask me a question ! :star:"}
    ]


# fuctions append message session history
def add_to_message_history(role, content):
    message = {"role": role, "content": str(content)}
    st.session_state["messages"].append(
        message
    )


# Initiate Chat Engin : SimpleChatEngine
if "chat_engine" not in st.session_state:
    # st.session_state["chat_engine"] = Groq(model=model_llama, api_key=api_key)
    st.session_state["chat_engine"] = SimpleChatEngine.from_defaults()

# Display the prior chat messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    if not api_key:
        st.info("Please add your GROQ API key to continue.")
        st.stop()

    add_to_message_history("user", prompt)
    # Display the new question immediately after it is entered
    with st.chat_message("user"):
        st.write(prompt)
    # If last message is not from assistant, generate a new response
    # if st.session_state["messages"][-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = st.session_state["chat_engine"].stream_chat(prompt)
        response_str = ""
        response_container = st.empty()
        for token in response.response_gen:
            response_str += token
            response_container.write(response_str)
        # st.write(response.response)
        add_to_message_history("assistant", response.response)

    # Save the state of the generator
    st.session_state["response_gen"] = response.response_gen
