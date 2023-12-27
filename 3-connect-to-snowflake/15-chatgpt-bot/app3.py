import re, streamlit as st
from openai import OpenAI
from prompts import get_system_prompt, get_prompt_questions

# chatbot agent with OpenAI, Streamlit and Snowflake Marketplace data
def chat(client):
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]

    #if prompt := st.chat_input():
    #    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt = st.selectbox("Select a question:", get_prompt_questions(), index=None)
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "results" in message:
                st.dataframe(message["results"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            response = ""
            resp_container = st.empty()
            for delta in client.chat.completions.create(
                stream=True,
                model="gpt-3.5-turbo",
                messages=([{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages])):
                response += (delta.choices[0].delta.content or "")
                resp_container.markdown(response)

            message = {"role": "assistant", "content": response}
            sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
            if sql_match:
                sql = sql_match.group(1)
                conn = st.connection("snowflake")
                message["results"] = conn.query(sql)
                st.dataframe(message["results"])
            st.session_state.messages.append(message)


if __name__ == "__main__":
    st.title("ChatGPT Bot")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    chat(client)