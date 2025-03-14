import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from helpful import format_followers, format_percent, format_percent_change, RELIGIOUS_COLORS

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
        label = st.radio("Show value  as", options = ["Number", "Percent"])
        minyear, maxyear = st.slider("Year", min_value=1950, max_value=cdf["Year"].max(), value = (1950, cdf["Year"].max()), step = 5)
        country = st.selectbox("Country", options= ["All Countries"] + sorted(list(cdf["Country"].unique())))
        religions = st.multiselect("Religions", options= sorted(list(cdf["Religion"].unique())))

# Data Filtering
if country != "All Countries":
    cdf = cdf[cdf["Country"] == country]
cdf = cdf[(cdf["Year"] >= minyear) & (cdf["Year"] <= maxyear)]
df = cdf.groupby(["Year", "Religion"])["Followers"].sum().reset_index()
sorted_religions = df.groupby("Religion")["Followers"].sum().sort_values(ascending=False).index.tolist()
colors = {c: RELIGIOUS_COLORS.get(c) for c in sorted_religions}
df["YearTotal"] = df.apply(lambda row: df[df["Year"]==row["Year"]]["Followers"].sum(), axis=1)
df["Percent"] = (df["Followers"] / df["YearTotal"])
df["Formatted_Percent"] = df["Percent"].apply(format_percent)
df["Formatted_Followers"] = df["Followers"].apply(format_followers)
df["Previous_Followers"] = df.apply(lambda row: find_previous_followers(row, df), axis=1)
df["Percent_Change"] = np.where(
    df["Previous_Followers"].isna(),
    None,
    (df["Followers"] - df["Previous_Followers"]) / df["Previous_Followers"]
)
df["Percent_Change_Formatted"] = df["Percent_Change"].apply(format_percent_change)

if religions:
    df = df[df["Religion"].isin(religions)]

if label == "Number":

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
        y="Percent", 
        color="Religion", 
        title="Percent of Major Religions Over Time", 
        labels={"Percent": "Percent", "Year": "Year"},
        line_shape="linear",
        color_discrete_map=colors,
        category_orders={"Religion": sorted_religions},
        text = "Formatted_Percent"
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
            title="Percent",
            range=[0,df["Percent"].max() + 0.05],
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
    table_df = df[["Religion","Year", "Followers", "Percent"]]
    table_df["Year"] = table_df["Year"].astype(str)
    table_df.sort_values(by = ["Religion", "Year"], inplace=True)
    table_df.rename(columns={"Percent": "Percent"}, inplace =True)
    
    styled_df = table_df.style.format({
        "Followers": format_followers,
        "Percent": format_percent
    })
    st.dataframe(styled_df, hide_index=True, use_container_width=True)