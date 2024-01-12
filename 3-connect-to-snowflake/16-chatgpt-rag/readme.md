# Create a ChatGPT Agent for Your Web Pages

With ChatGPC already connected, and with the chat already created before, simplifies the [**Build a Retrieval Augmented Generation(RAG) based LLM assistant using Streamlit, OpenAI and LlamaIndex**](https://quickstarts.snowflake.com/guide/build_rag_based_blog_ai_assistant_using_streamlit_openai_and_llamaindex/index.html?index=..%2F..index#0) quickstart guide, by building a ChatGPT agent answering questions about content in your own web pages. Original [**GitHub repository** is here](https://github.com/Snowflake-Labs/sfguide-blog-ai-assistant). There will be no connection to Snowflake or any other database this time.

## Files

* **1-download.py** - downloads in the *pages/* folder web pages as markdown files, using Chromium. Run with "python 1-download.py".
* **2-index.py** - with the files from *pages/*, builds a Llama index in *index/*, using OpenAI. Run with "python 1-index.py".
* **3-app.py** - chatbot agent with ChatGPT, answering question related to the *index/* files. Run with "streamlit run 3-app.py".
* **requirements.txt** - local dependencies (including *openai*). Must execute first!

## Actions

Create first an OpenAI account and get an API key, to use the remote service. Save it in the *.streamlit/secrets.toml* file (never push this file into GitHub!).

From the local subfolder, run **`pip install -r requirements.txt`**, to install all the required libraries.

Cleanup all *pages/* and *index/* subfolders, if they are not already empty.

Run in a Terminal window **`python 1-download.py`**, which will download Chromium (if not already downloaded), to execute and download web pages that you can change in the PAGES array. They will be saved as MD markdown files in the *pages/* folder.

Run in a Terminal window **`python 2-index.py`**, which will create a Llama index in *index/* for the MD files from the *pages/* folder.

Run in a Terminal window **`streamlit run 3-app.py`**, for a ChatGPT agent loading the files from *index/* as the query engine. Ask basic questions about Snowpark from these files, such as "***How to load a table into a dataframe?***". Quit the local Streamlit web app session with CTRL+C.
