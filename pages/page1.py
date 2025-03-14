import streamlit as st
import plotly.express as px
from helpful import format_followers, format_percent

st.title(":material/counter_1: Major Religions")
st.write("What religions are most widely practiced around the world?")


cdf = st.session_state.cdf

vis,fil = st.columns([6,2])
with fil:
    with st.container(border=True):
        st.write(":material/settings: Settings")
        year = st.slider("Year", min_value=cdf["Year"].min(), max_value=cdf["Year"].max(), value = cdf["Year"].max(), step = 5)
        country = st.selectbox("Country", options= ["All Countries"] + list(cdf["Country"].unique()))
        c1,c2 = st.columns(2)
        labels = c1.radio("Show label as", options = ["Number", "Percent"])
        labels = "Formatted_Followers" if labels == "Number" else "Formatted_Percent"
        sortby = c2.radio("Sort by", options = ["Followers", "Religion"])

if country != "All Countries":
    cdf = cdf[cdf["Country"] == country]
df = cdf[cdf["Year"] == year].groupby("Religion")["Followers"].sum().reset_index()
df = df.sort_values(by=sortby, ascending=sortby == "Followers") 
df["Percent"] = (df["Followers"] / df["Followers"].sum())
df["Formatted_Followers"] = df["Followers"].apply(format_followers)
df["Formatted_Percent"] = df["Percent"].apply(format_percent)
max_followers = df["Followers"].max()
df["FontSize"] = df["Followers"].apply(lambda x: 12 + (x / max_followers) * 20) 
df["BarWidth"] = df["Followers"].apply(lambda x: 0.4 + (x / max_followers) * 0.4) 


fig = px.bar(
    df,
    x="Followers",
    y="Religion",
    title=f"Religion Affiliation ({country} - {year})",
    text="Followers",
    labels={"Followers": "Number of Followers", "Religion": "Religion"},
    orientation="h",
    color="Followers",
    color_continuous_scale=["lightgrey", "darkblue"], 
)
fig.update_layout(
    showlegend=False,
    height=675,
    width=900,
    xaxis_title="Followers",
    yaxis_title=None,
    yaxis = dict(
        tickmode="array",
        tickvals=df["Religion"],
        ticktext=[
            f'<span style="font-size:{size}px">{religion}</span>' 
            for religion, size in zip(df["Religion"], df["FontSize"])
        ],
        tickfont=dict(
            color="black",
            size=14,
            weight="bold"
        )
    ),
        xaxis=dict(
        range=[0, max_followers* 1.4]
    ),
    title_x=0.2,
    title_font=dict(
        size=24,
        color="grey"
    ),
    coloraxis_showscale=False,
    hovermode=False,
    dragmode=False
)
fig.update_traces(
    textposition="outside",
    customdata = df[labels],
    texttemplate="%{customdata}",
    width=df["BarWidth"].tolist()
)

with vis:
    st.plotly_chart(fig)