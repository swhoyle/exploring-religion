import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")



@st.cache_data
def get_data():
    gdf = pd.read_csv("data/global.csv")
    ndf = pd.read_csv("data/national.csv")
    rdf = pd.read_csv("data/regional.csv")
    return gdf, ndf, rdf

gdf, ndf, rdf = get_data()

def page1():
    st.title("Major Religions")
    st.write("What religions are most widely practiced around the world?")

def page2():
    st.title("Geographic Distribution")
    st.write("How does religious affiliation differ across countries and regions?")

def page3():
    st.title("Historical Trends")
    st.write("Are major religious practices increasing or decreasing over time?")

def page4():
    st.title("Belief Comparisons")
    st.write("What similarities and differences exist among major religious beliefs and practices?")

def page5():
    st.title("Branches of Religions")
    st.write("What are sub-religions or denominations within major religions?")


def home_page():
    st.title("Exploring Religion")
    st.write("This project aims to explore and visualize global religious trends, demographics, and correlations. By leveraging compelling data visualizations, the project will help foster a deeper understanding of various religions and their societal impact.")
    st.subheader("Tasks")
    st.markdown("""
1. **<u>Major Religions</u>**: What religions are most widely practiced around the world?  
2. **<u>Geographic Distribution</u>**: How does religious affiliation differ across countries and regions?  
3. **<u>Historical Trends</u>**: Are major religious practices increasing or decreasing over time?  
4. **<u>Belief Comparisons</u>**: What similarities and differences exist among major religious beliefs and practices?  
5. **<u>Branches of Religions</u>**: What are sub-religions or denominations within major religions?  
""", unsafe_allow_html=True)


def data_page():
    st.title("Data")
    st.write(f"https://www.kaggle.com/datasets/umichigan/world-religions")
    gtab, ntab, rtab = st.tabs(["global.csv", "national.csv", "regional.csv"])
    with gtab:
        st.dataframe(rdf.style.format({"year": "{:.0f}"}), hide_index=True)
    with ntab:
        st.dataframe(ndf.style.format({"year": "{:.0f}"}), hide_index=True)
    with rtab:
        st.dataframe(rdf.style.format({"year": "{:.0f}"}), hide_index=True)

if 'page' not in st.session_state:
    st.session_state.page = 0

PAGES = {
    "Home": home_page,
    "Major Religions": page1,
    "Geographic Distribution": page2,
    "Historical Trends": page3,
    "Belief Comparisons": page4,
    "Branches of Religions": page5,
    "Data": data_page
}

st.sidebar.subheader("Pages")
page = st.sidebar.radio(
    "Pages",
    options = list(PAGES.keys()), 
    label_visibility="collapsed"
)

# show the page
PAGES[page]()