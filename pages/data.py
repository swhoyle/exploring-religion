import streamlit as st

session = st.session_state

st.title(":material/database: Data")
st.write(f"https://www.kaggle.com/datasets/umichigan/world-religions")
gtab, ntab, rtab, ctab, btab = st.tabs(["global.csv", "national.csv", "regional.csv", "cleaned.csv", "beliefs.csv"])
with gtab:
    st.dataframe(session.gdf.style.format({"year": "{:.0f}"}), hide_index=True)
with ntab:
    st.dataframe(session.ndf.style.format({"year": "{:.0f}"}), hide_index=True)
with rtab:
    st.dataframe(session.rdf.style.format({"year": "{:.0f}"}), hide_index=True)
with ctab:
    st.dataframe(session.cdf.head(1000).style.format({"year": "{:.0f}"}), hide_index=True, use_container_width=True)
with btab:
    st.dataframe(session.bdf.style.format({"year": "{:.0f}"}), hide_index=True, use_container_width=True)
