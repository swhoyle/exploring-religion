import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from helpful import format_followers, format_percent_change, RELIGIOUS_COLORS

def find_previous_followers(row, df):
    newdf = df[(df["Religion"] == row["Religion"]) & (df["Year"] == row["Year"] - 5)]
    if not newdf.empty:
        return newdf["Followers"].iloc[0]
    return None

st.title(":material/counter_3: Historical Trends")
st.write("Are major religious practices increasing or decreasing over time?")

cdf: pd.DataFrame = st.session_state.cdf

vis,space,fil = st.columns([6,0.2,2])

with fil:
    with st.container(border=True):
        st.write(":material/settings: Settings")
        label = st.radio("Show value  as", options = ["Religious Affiliation", "Percent Change"])
        minyear, maxyear = st.slider("Year", min_value=1950, max_value=cdf["Year"].max(), value = (1950, cdf["Year"].max()), step = 5)
        country = st.selectbox("Country", options= ["All Countries"] + sorted(list(cdf["Country"].unique())))
        religions = st.multiselect("Religions", options= sorted(list(cdf["Religion"].unique())))

# Data Filtering
if country != "All Countries":
    cdf = cdf[cdf["Country"] == country]
if religions:
    cdf = cdf[cdf["Religion"].isin(religions)]
cdf = cdf[(cdf["Year"] >= minyear) & (cdf["Year"] <= maxyear)]
df = cdf.groupby(["Year", "Religion"])["Followers"].sum().reset_index()
sorted_religions = df.groupby("Religion")["Followers"].sum().sort_values(ascending=False).index.tolist()
colors = {c: RELIGIOUS_COLORS.get(c) for c in sorted_religions}
df["Formatted_Followers"] = df["Followers"].apply(format_followers)
df["Previous_Followers"] = df.apply(lambda row: find_previous_followers(row, df), axis=1)
df["Percent_Change"] = np.where(
    df["Previous_Followers"].isna(),
    None,
    (df["Followers"] - df["Previous_Followers"]) / df["Previous_Followers"]
)
df["Percent_Change_Formatted"] = df["Percent_Change"].apply(format_percent_change)

if label == "Religious Affiliation":

    fig = px.line(df, 
        x="Year", 
        y="Followers", 
        color="Religion", 
        title="Followers of Major Religions Over Time", 
        labels={"Followers": "Number of Followers", "Year": "Year"},
        line_shape="linear",
        color_discrete_map=colors,
        category_orders={"Religion": sorted_religions},
        text = "Formatted_Followers"
    )

    fig.update_layout(
        width=1000,
        height=600,
        hovermode="x unified",
        title_font=dict(
            size=20,
            color="grey"
        ),
        title_x=0.3,
        yaxis=dict(
            title="Followers",
            range=[0, df["Followers"].max() * 1.2],
            showgrid=True
        )
    )
    fig.update_traces(
        mode="markers+lines",
        line=dict(width=1),
        marker=dict(symbol="circle", size=6),
        hovertemplate="<b>%{text}</b>"
    )

else:

    fig = px.line(df, 
        x="Year", 
        y="Percent_Change", 
        color="Religion", 
        title="Percent Change of Major Religions Over Time", 
        labels={"Percent_Change": "Percent Change", "Year": "Year"},
        line_shape="linear",
        color_discrete_map=colors,
        category_orders={"Religion": sorted_religions},
        text = "Percent_Change_Formatted"
    )

    fig.update_layout(
        width=1000,
        height=600,
        hovermode="x unified",
        title_font=dict(
            size=20,
            color="grey"
        ),
        title_x=0.3,
        yaxis=dict(
            title="Percent Change",
            range=[df["Percent_Change"].min() - abs(df["Percent_Change"].min()) * 0.5,
                   df["Percent_Change"].max() + abs(df["Percent_Change"].max()) * 0.3],
            showgrid=True,
            tickformat=".0%"
        )
    )
    fig.update_traces(
        mode="markers+lines",
        line=dict(width=1),
        marker=dict(symbol="circle", size=6),
        hovertemplate="<b>%{text}</b>"
    )

with vis:
    st.plotly_chart(fig)
    table_df = df[["Religion","Year", "Followers", "Percent_Change"]]
    table_df["Year"] = table_df["Year"].astype(str)
    table_df.sort_values(by = ["Religion", "Year"], inplace=True)
    table_df.rename(columns={"Percent_Change": "Percent Change (5 Years Ago)"}, inplace =True)
    
    styled_df = table_df.style.format({
        "Followers": format_followers,
        "Percent Change (5 Years Ago)": format_percent_change
    })
    st.dataframe(styled_df, hide_index=True, use_container_width=True)