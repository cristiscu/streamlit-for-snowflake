import streamlit as st
from llama_index import ServiceContext, SimpleDirectoryReader, TreeIndex
from llama_index.llms.openai import OpenAI

import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

(TreeIndex.from_documents(
    SimpleDirectoryReader("./pages").load_data(),
    service_context=ServiceContext.from_defaults(
        llm=OpenAI(api_key=st.secrets["OPENAI_API_KEY"])))
    .storage_context
    .persist(persist_dir="./index"))
