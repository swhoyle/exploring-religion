import streamlit as st

session = st.session_state

st.title(":material/database: Data")
st.write(f"https://www.kaggle.com/datasets/umichigan/world-religions")
gtab, ntab, rtab = st.tabs(["global.csv", "national.csv", "regional.csv"])
with gtab:
    st.dataframe(session.rdf.style.format({"year": "{:.0f}"}), hide_index=True)
with ntab:
    st.dataframe(session.ndf.style.format({"year": "{:.0f}"}), hide_index=True)
with rtab:
    st.dataframe(session.rdf.style.format({"year": "{:.0f}"}), hide_index=True)
