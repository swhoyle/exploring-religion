import streamlit as st
import pandas as pd

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

session = st.session_state

@st.cache_data
def get_data():
    print("reading data...")
    gdf = pd.read_csv("data/global.csv")
    ndf = pd.read_csv("data/national.csv")
    rdf = pd.read_csv("data/regional.csv")
    return gdf, ndf, rdf

session.gdf, session.ndf, session.rdf = get_data()

pages = [
        st.Page("pages/home.py", title="Home", icon = ":material/home:"),
        st.Page("pages/page1.py", title="Major Religions", icon = ":material/counter_1:"),
        st.Page("pages/page2.py", title="Geographic Distribution", icon = ":material/counter_2:"),
        st.Page("pages/page3.py", title="Historical Trends", icon = ":material/counter_3:"),
        st.Page("pages/page4.py", title="Belief Comparisons", icon = ":material/counter_4:"),
        st.Page("pages/page5.py", title="Branches of Religions", icon = ":material/counter_5:"),
        st.Page("pages/data.py", title="Data", icon = ":material/database:")
    ]

pg = st.navigation(pages)
pg.run()