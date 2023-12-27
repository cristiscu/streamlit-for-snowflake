import streamlit as st
from openai import OpenAI

# chat with OpenAI and Streamlit
def chat(client):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How can I help?"}]

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                r = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=([{"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages]))
                response = r.choices[0].message.content
                st.write(response)

        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)


if __name__ == "__main__":
    st.title("ChatGPT Bot")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    chat(client)