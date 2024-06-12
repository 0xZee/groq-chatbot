import streamlit as st
from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.chat_engine import SimpleChatEngine

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import PromptTemplate


## Setting LLM
def set_llm_embed(api_key):
    # LLM
    model_llama = "llama3-8b-8192"
    model_gemma = "gemma-7b-it"
    model_mixtral = "mixtral-8x7b-32768"
    model_whistper = "whisper-large-v3"
    # set GROQ LLM
    LLM_GROQ = Groq(model=model_mixtral,temperature=0.2, api_key=api_key)
    Settings.llm = LLM_GROQ
    # Set Cohere Embeddings
    COHERE_API = st.secrets['COHERE_API']
    ## Setting Embeddings
    #EMBED_HF = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    EMBED_CO = CohereEmbedding(cohere_api_key=COHERE_API,
                            model_name="embed-multilingual-v3.0", input_type="search_query",)
    Settings.embed_model = EMBED_CO


#### Set ChatEngine : Simple Chat Mode
def set_simple_chat_engine(api_key):
  LLM_GROQ = Groq(model="llama3-8b-8192", temperature=0.5, api_key=api_key)
  chat_engine = SimpleChatEngine.from_defaults(
      llm=LLM_GROQ,
      memory = ChatMemoryBuffer.from_defaults(token_limit=4096),
      system_prompt=("""
      You are a kind and talkative chatbot, able to have normal interactions, as well as providing low-level detailed responses.\n
      \nInstruction: Use the previous chat history, to interact and help the user.
      """),
      verbose=True)
  return chat_engine
