import streamlit as st
from comp.functions import set_simple_chat_engine


#### UI
#### page config
st.set_page_config(page_title="Groq ChatBot", page_icon=":space_invader:",
                   layout="centered", initial_sidebar_state="auto", menu_items=None)


#### sidebar
with st.sidebar:
    st.subheader("🤖 :orange-background[0xZee] Groq Llama3 ChatBot", divider="orange")
    st.subheader("🔐 GROQ INFERENCE API", divider="grey")
    if ("GROQ_API" in st.secrets and st.secrets['GROQ_API'].startswith('gsk_')):
        st.success(':white_check_mark: GROQ API ')
        st.success(':white_check_mark: LLM Llama3')
        api_key = st.secrets['GROQ_API']
    else:
        api_key = st.text_input('Enter your Groq API Key', type='password')
        if not (api_key.startswith('gsk_') and len(api_key) == 56):
            st.warning("Enter a Valid GROQ API key")
        else:
            st.success('GROQ API Key Provided')

    st.subheader("⚙️ CHAT SESSION PARAM.", divider="grey")
    if st.button("Clear Chat Session", use_container_width=True, type="primary"):
        st.session_state["messages"] = [
            {"role": "assistant", "content": ":sparkles: Hi, I'm here to help, How can I assist you today ? :star:"}]

    if st.button("Clear Chat Memory", use_container_width=True, type="secondary"):
        st.session_state["chat_engine"].reset()
    st.text("")
    st.text("")
    st.text("💻 https://github.com/0xZee/groq-chatbot/")


#### main page
with st.container(border=True):
    c1, c2 = st.columns([1, 6])
    with c1:
        st.image("./media/zee.jpg", width=60)
    with c2:
        st.subheader(
            "💬 :orange-background[GROQ] :orange[CHATBOT] 🤖 ", divider='orange')


#### Function Append message history
def add_to_message_history(role, content):
    message = {"role": role, "content": str(content)}
    st.session_state["messages"].append(
        message
    )
####
#### CHAT SESSION

if api_key:
    try:
        # Set chat engin
        if "chat_engine" not in st.session_state:
            try:
                st.session_state["chat_engine"] = set_simple_chat_engine(api_key=api_key)
            except Exception as e:
                st.error(f"error occurred in setting chat engine : {e}")
        # Initialize the chat messages history
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Ask me a question or tell me what comes in your mind !"}
            ]
        # Display the prior chat messages
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        ## Prompting
        ## Prompt for user input and save to chat history
        if prompt := st.chat_input("Your question"):
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
                    response_container.markdown(response_str)
                #st.write(response.source)
                add_to_message_history("assistant", response.response)

            # Save the state of the generator
            st.session_state["response_gen"] = response.response_gen
        #
        #
    except Exception as e:
        st.error(f"error occurred in chat session : {e}")


