# Integrate Snowflake with ChatGPT

Registers with and connects to OpenAI API, with an API key. Then creates a simple chat, using the *st.chat_input* and *st.chat_message* Streamlit controls. Finally, simplifies the [**Frosty: Build an LLM Chatbot in Streamlit on your Snowflake Data**](https://quickstarts.snowflake.com/guide/frosty_llm_chatbot_on_streamlit_snowflake/index.html?index=..%2F..index#0) quickstart guide, by building a ChatGPT agent generating SQL statements for some free Snowflake Marketplace datasets. We'll be using the same  [**Financial & Economic Essentials, by Cybersyn, Inc**] dataset.

## Files

* **app1.py** - connects to OpenAI API, with an API key saved in the */streamlit/secrets.toml* file.
* **app2.py** - simple chat using the *st.chat_input* and *st.chat_message* Streamlit controls.
* **app3.py** - chatbot agent with OpenAI, Streamlit and Snowflake Marketplace data.
* **prompts.py** - initial instructions to send to ChatGPT, to act as a Frosty agent and generate SQL statements for some views.
* **setup.sql** - create some views on top of the free Marketplace datasets.
* **requirements.txt** - local dependencies (including *openai*).

## Other ChatGPT-based tutorials with Snowflake

* [**Getting Started with Generative AI in Snowflake and Streamlit**](https://quickstarts.snowflake.com/guide/getting_started_with_generative_ai_snowflake_external_functions/index.html?index=..%2F..index#0)
* [**Build a Retrieval Augmented Generation(RAG) based LLM assistant using Streamlit, OpenAI and LlamaIndex**](https://quickstarts.snowflake.com/guide/build_rag_based_blog_ai_assistant_using_streamlit_openai_and_llamaindex/index.html?index=..%2F..index#0)
* [**A Image Recognition App in Snowflake using Snowpark Python, PyTorch, Streamlit and OpenAI**](https://quickstarts.snowflake.com/guide/image_recognition_snowpark_pytorch_streamlit_openai/index.html?index=..%2F..index#0)
