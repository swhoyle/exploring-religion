import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from helpful import format_followers, format_percent, RELIGIOUS_COLORS,RELIGIOUS_COLORS_LIGHT

st.title(":material/counter_5: Branches of Religions")
st.write("What are sub-religions or denominations within major religions?")

vis,fil = st.columns([6,2])
cdf: pd.DataFrame = st.session_state.cdf

with fil:
    with st.container(border=True):
        st.write(":material/settings: Settings")
        year = st.slider("Year", min_value=1950, max_value=cdf["Year"].max(), value = cdf["Year"].max(), step = 5)
        country = st.selectbox("Country", options= ["All Countries"] + sorted(list(cdf["Country"].unique())))
        religions = st.multiselect("Religions", options= sorted(list(cdf[~cdf["Subreligion"].isna()]["Religion"].unique())))

# Data Filtering
if country != "All Countries":
    cdf = cdf[cdf["Country"] == country]
if religions:
    cdf = cdf[cdf["Religion"].isin(religions)]
cdf = cdf[(cdf["Year"] == year)]

df = cdf.groupby(["Religion", "Subreligion"])["Followers"].sum().reset_index()
df["ReligionFollowers"] = df.apply(
    lambda row: df[df["Religion"] == row["Religion"]]["Followers"].sum(), 
    axis=1
)
df = df.sort_values(by = ["ReligionFollowers","Followers"], ascending=False)
df["SubreligionNode"] = df["Religion"] + "-" + df["Subreligion"]
df["Percent_All"] = round((df["Followers"] / df["Followers"].sum()) * 100,2)
df["Percent_Religion"] = df.apply(
    lambda row: round((row["Followers"] / df[df["Religion"] == row["Religion"]]["Followers"].sum()) * 100, 2), 
    axis=1
)
df["Formatted_Followers"] = df["Followers"].apply(format_followers)
df["Formatted_Percent_All"] = df["Percent_All"].apply(format_percent)
df["Formatted_Percent_Religion"] = df["Percent_Religion"].apply(format_percent)
df["Width"] = df["Percent_All"].apply(lambda x: max(x, 1))
df["Color"] = df["Religion"].map(RELIGIOUS_COLORS)
nodes = pd.concat([df["Religion"], df["SubreligionNode"]]).unique()
node_indices = {node: i for i, node in enumerate(nodes)}

# Source and target indices for Sankey diagram
source = df["Religion"].map(node_indices)
target = df["SubreligionNode"].map(node_indices)

# Create the Sankey Diagram
fig = go.Figure(data=[go.Sankey(
    arrangement = "snap",
    textfont = dict(
        family = "Times New Roman",
        size=16,
        color="black",
        shadow=False,
        weight = "bold"
    ),
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0),
        label=[node.split('-')[1] if '-' in node else node for node in nodes],
        color=[RELIGIOUS_COLORS.get(node.split('-')[0], "lightgray") for node in nodes],
        hoverinfo="none"
        
    ),
    link=dict(
        arrowlen=0,
        color = [RELIGIOUS_COLORS_LIGHT.get(nodes[i].split('-')[0], "lightgray") for i in source],
        source=source,  
        target=target,
        value=df["Width"],
        customdata=df["Formatted_Percent_Religion"],
        hovertemplate="%{customdata} of %{source.label} is made up of sub-religion %{target.label}",
        #hoverinfo="skip",
        hovercolor=[RELIGIOUS_COLORS.get(nodes[i].split('-')[0], "lightgray") for i in source],
        hoverlabel=dict(
            bgcolor="black",
            font=dict(color="white", size=10),
            align = "left"
        )
    ))]
)

fig.update_layout(
    title_text=f"Major Religions and Subreligions ({country} - {year})",
    height = 700,
    width = 700,
    title_x=0,
    title_font=dict(
        size=24,
        color="grey"
    )
)

with vis:
    st.plotly_chart(fig)

with vis:
    table_df = df[["Religion", "Subreligion", "Followers", "Percent_Religion","Percent_All"]]
    table_df.rename(columns={"Percent_Religion":"Percent on Religion", "Percent_All": "Percent of All"}, inplace = True)
    styled_df = table_df.style.format({
        "Followers": format_followers,
        "Percent on Religion": format_percent,
        "Percent of All": format_percent
    })
    st.dataframe(styled_df, hide_index=True, use_container_width=True)
