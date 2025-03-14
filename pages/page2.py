import streamlit as st
import plotly.express as px
import pandas as pd
from helpful import format_followers, format_percent, RELIGIOUS_COLORS

st.title(":material/counter_2: Geographic Distribution")
st.write("How does religious affiliation differ across countries and regions?")

vis,fil = st.columns([6,2])

cdf: pd.DataFrame = st.session_state.cdf

with fil:
    with st.container(border=True):
        st.write(":material/settings: Settings")
        label = st.radio("Show value  as", options = ["Religious Affiliation", "Most Popular Religion"])
        year = st.slider("Year", min_value=cdf["Year"].min(), max_value=cdf["Year"].max(), value = cdf["Year"].max(), step = 5)
        if label == "Religious Affiliation":
            religion_filter = st.selectbox("Religion", options=["All Religions"] + list(cdf["Religion"].unique()))
        else:
            religion_filter = "All Religions"

        if religion_filter != "All Religions":
            cdf = cdf[cdf["Religion"] == religion_filter]

        cdf = cdf[cdf["Year"]==year]

if label == "Religious Affiliation":

    df = cdf.groupby(["Country", "Country Code"])["Followers"].sum().reset_index()
    df["Percent"] = round((df["Followers"] / df["Followers"].sum()) * 100,2)
    df["Formatted_Followers"] = df["Followers"].apply(format_followers)
    df["Formatted_Percent"] = df["Percent"].apply(format_percent)

    fig = px.choropleth(df, 
        locations="Country Code", 
        color="Followers",
        hover_name="Country Code",
        color_continuous_scale=["lightgrey", "darkblue"],
        projection="natural earth",
        title=f"Religious Affiliation by Country ({religion_filter} - {year})"
    )

    fig.update_layout(
        title_font=dict(
            size=20,
            color="grey"
        ),
        title_x=0.15
    )

    table_df = df.sort_values(by = "Followers", ascending=False)[["Country", "Country Code", "Formatted_Followers", "Formatted_Percent"]]
    table_df = table_df.rename(columns = {"Formatted_Followers": "Followers", "Formatted_Percent": "Percent"})

    with vis:
        st.plotly_chart(fig)
        st.dataframe(
            table_df,
            hide_index=True,
            use_container_width=True
        )

else:
    df = cdf.groupby(["Country", "Country Code", "Religion"])["Followers"].sum().reset_index()
    df_most_popular = df.loc[df.groupby(["Country", "Country Code"])["Followers"].idxmax(), ["Country", "Country Code", "Religion"]]

    
    df_most_popular["Color"] = df_most_popular["Religion"].map(RELIGIOUS_COLORS)
    religion_counts = df_most_popular["Religion"].value_counts()
    sorted_religions = religion_counts.index.tolist()
    religion_counts_df = religion_counts.reset_index()
    religion_counts_df["Percent"] =  round((religion_counts_df["count"] / religion_counts_df["count"].sum()) * 100,2)
    religion_counts_df["Formatted_Percent"] = religion_counts_df["Percent"].apply(format_percent)
    religion_counts_df = religion_counts_df.rename(columns = {"count": "Number of Countries", "Formatted_Percent": "%"})
    fig = px.choropleth(df_most_popular, 
        locations="Country Code", 
        color="Religion",
        hover_name="Country",
        title=f"Most Popular Religion by Country ({year})",
        color_discrete_map=RELIGIOUS_COLORS,
        projection="natural earth",
        category_orders={"Religion": sorted_religions}
    )
    fig.update_layout(
        title_font=dict(
            size=20,
            color="grey"
        ),
        title_x=0.3,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.7,
            xanchor="left",
            x=0
        )
    )

    table_df = df_most_popular[["Country", "Country Code", "Religion"]]
    table_df = table_df.rename(columns={"Religion": "Most Popular Religion"})

    with vis:
        st.plotly_chart(fig)
        c1, c2 = st.columns(2)
        c1.dataframe(table_df, hide_index=True,use_container_width=True)
        c2.dataframe(religion_counts_df[["Religion", "Number of Countries", "%"]], hide_index=True,use_container_width=True)


