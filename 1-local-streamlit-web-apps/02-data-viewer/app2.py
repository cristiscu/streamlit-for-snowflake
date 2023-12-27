import streamlit as st

st.title("Hierarchical Data Viewer")
st.header("this is a header")
st.subheader("subheader")
st.caption("caption")

st.write("this is write")
st.text("fixed text")
st.code("v = variable()\nanother_call()", "python")
st.markdown("*bold*")
st.divider()

st.latex("...")

st.error("this is an error")
st.info("this is info")
st.warning("this is a warning")
st.success("this is success")

#st.balloons()
#st.snow()