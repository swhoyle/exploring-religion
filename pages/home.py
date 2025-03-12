import streamlit as st

session = st.session_state

st.title(":material/church: Exploring Religion")
st.write("This project aims to explore and visualize global religious trends, demographics, and correlations to help foster a deeper understanding of various religions and their societal impact")
st.caption("**Intended Stakeholders**: General public seeking knowledge about world religions or researchers looking to analyze religous demographics and trends")
st.subheader("Tasks")
st.markdown("""
1. **<u>Major Religions</u>**: What religions are most widely practiced around the world?  
2. **<u>Geographic Distribution</u>**: How does religious affiliation differ across countries and regions?  
3. **<u>Historical Trends</u>**: Are major religious practices increasing or decreasing over time?  
4. **<u>Belief Comparisons</u>**: What similarities and differences exist among major religious beliefs and practices?  
5. **<u>Branches of Religions</u>**: What are sub-religions or denominations within major religions?  
""", unsafe_allow_html=True)

st.subheader("Data")
st.write(f"https://www.kaggle.com/datasets/umichigan/world-religions")
gtab, ntab, rtab = st.tabs(["global.csv", "national.csv", "regional.csv"])
with gtab:
    st.dataframe(session.rdf.style.format({"year": "{:.0f}"}), hide_index=True)
with ntab:
    st.dataframe(session.ndf.style.format({"year": "{:.0f}"}), hide_index=True)
with rtab:
    st.dataframe(session.rdf.style.format({"year": "{:.0f}"}), hide_index=True)