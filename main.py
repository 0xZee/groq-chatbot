import streamlit as st
from groq import Groq

st.set_page_config(page_title="Groq ChatBot", page_icon=":robot_face:",
                   layout="centered", initial_sidebar_state="auto", menu_items=None)

with st.sidebar:
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

    st.subheader("Model Buffer Memory", divider="grey")
    memory_buffer = st.slider("Memory Buffer Size",
                              min_value=1, max_value=10, value=4)

with st.container(border=True):
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader(
            "💬 :violet-background[GROQ] :violet[CHATBOT]", divider='violet')
    with c2:
        st.subheader(f"🤖 :violet-background[{user_model}]", divider='violet')

# function


def generate_response():
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user",
             "content": query}
        ],
        model=user_model
    )

    return chat_completion.choices[0].message.content


#


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm Groq ChatBot, How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not api_key:
        st.info("Please add your GROQ API key to continue.")
        st.stop()

    client = Groq(api_key=api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response = client.chat.completions.create(
    #   model="gpt-3.5-turbo", messages=st.session_state.messages)
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}], model=user_model)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
