import streamlit as st
import pandas as pd

st.title(":material/counter_4: Belief Comparisons")
st.write("What similarities and differences exist among major religious beliefs and practices?")

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from itertools import combinations

c1,c2 = st.columns([6,2])

# Define the data for the religions comparison dataset
data = [
    ['Christianity', 'Monotheistic', 'Yes', 'Middle East', '30 CE', 'Early Common Era (500 BCE - 500 CE)', 'Heaven/Hell', ['Prayer', 'Sacraments'], 'Weekly', 'Priests'],
    ['Judaism', 'Monotheistic', 'Yes', 'Middle East', '1800 BCE', 'Ancient (2000 BCE - 1000 BCE)', 'Olam Ha-Ba', ['Prayer', 'Rituals'], 'Daily', 'Rabbis'],
    ['Islam', 'Monotheistic', 'Yes', 'Middle East', '610 CE', 'Early Common Era (500 BCE - 500 CE)', 'Heaven/Hell', ['Prayer', 'Fasting'], 'Daily', 'Imams'],
    ['Buddhism', 'Nontheistic', 'No', 'India', '5th century BCE', 'Classical (1000 BCE - 500 BCE)', 'Rebirth', ['Meditation', 'Chanting'], 'Daily', 'Monks'],
    ['Hinduism', 'Polytheistic', 'No', 'India', '1500 BCE', 'Ancient (2000 BCE - 1000 BCE)', 'Rebirth', ['Puja', 'Meditation'], 'Daily', 'Priests'],
    ['Sikhism', 'Monotheistic', 'No', 'India', '15th century', 'Middle Ages (500 CE - 1500 CE)', 'Rebirth', ['Prayer', 'Community Service'], 'Daily', 'Granthi'],
    ['Taoism', 'Polytheistic', 'Yes', 'China', '4th century BCE', 'Classical (1000 BCE - 500 BCE)', 'Immortality', ['Meditation', 'Rituals'], 'Daily', 'Priests'],
    ['Shinto', 'Polytheistic', 'Yes', 'Japan', '8th century CE', 'Early Common Era (500 BCE - 500 CE)', 'Spirits', ['Rituals', 'Festivals'], 'Seasonal', 'Priests']
]

# Define the columns
columns = ['Religion', 'Concept of Gods', 'Single Holy Book?', 'Origin', 'Origin Period', 'Origin Period Category', 'Afterlife Belief', 'Key Practices', 'Worship Frequency', 'Clergy Roles']

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Calculate similarity scores between religions
def calculate_similarity(row1, row2):
    matches = 0
    for col in columns[1:]:
        if isinstance(row1[col], list) and isinstance(row2[col], list):
            matches += len(set(row1[col]) & set(row2[col]))
        elif row1[col] == row2[col]:
            matches += 1
    return round(matches / (len(columns) - 1),2)

similarity_scores = []
for (i, row1), (j, row2) in combinations(df.iterrows(), 2):
    similarity = calculate_similarity(row1, row2)
    similarity_scores.append((row1['Religion'], row2['Religion'], similarity))

similarity_df = pd.DataFrame(similarity_scores, columns=['Religion 1', 'Religion 2', 'Similarity Score'])

fig = px.scatter(
    similarity_df,
    x='Religion 1',
    y='Religion 2',
    size='Similarity Score',
    color='Similarity Score',
    title='Similarity Between Religious Beliefs',
    color_continuous_scale=["red", "orange", "green", "darkgreen"]
)

fig.update_layout(
    width=1000,
    height=600,
    title_font=dict(
        size=20,
        color="grey"
    )
)


clicked_point = c1.plotly_chart(fig, use_container_width=True, on_select="rerun",selection_mode="points")

if clicked_point["selection"]["points"]:
    religion_1 = clicked_point["selection"]["points"][0]["x"]
    religion_2 = clicked_point["selection"]["points"][0]["y"]
    similarity_df = similarity_df[similarity_df["Religion 1"] == religion_1]
    similarity_df = similarity_df[similarity_df["Religion 2"] == religion_2]
    df = df[df["Religion"].isin([religion_1,religion_2])]

similarity_df = similarity_df.sort_values(by = "Similarity Score", ascending=False)

with c2:
    st.write("#")
    st.dataframe(similarity_df, hide_index=True, use_container_width=True)

st.subheader("Religious Belief Data")
st.dataframe(df, hide_index=True, use_container_width=True)