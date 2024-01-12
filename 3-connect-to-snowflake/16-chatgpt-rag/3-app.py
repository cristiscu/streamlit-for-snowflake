import streamlit as st
import openai
from llama_index import StorageContext, load_index_from_storage

openai.api_key = st.secrets["OPENAI_API_KEY"] 

st.title("ChatGPT Agent for Your Web Pages")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system",
        "content": ("Your purpose is to answer questions about specific documents only. "
        "Please answer the user's questions based on what you know about the document. "
        "If the question is outside scope of the document, please politely decline. "
        "If you don't know the answer, say `I don't know`.")}]

if "query_engine" not in st.session_state:
    st.session_state.query_engine = (load_index_from_storage(
            StorageContext.from_defaults(persist_dir="./index"))
        .as_query_engine())
    
for message in st.session_state.messages:
    if message["role"] not in ["user", "assistant"]: continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = st.session_state.query_engine.query(prompt)
        full_response = f"{response}"
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

