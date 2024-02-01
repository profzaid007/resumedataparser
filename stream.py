import streamlit as st
import pandas as pd
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt


csv_file = 'output_data.csv'
df = pd.read_csv(csv_file)


df['Skills'] = df['Skills'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])
df['Education'] = df['Education'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])


st.title('Resume Data Analysis App')


st.subheader('Resume Data')
st.dataframe(df)


st.subheader('Basic Statistics')
st.write(f"Total Resumes: {len(df)}")


st.subheader('Unique Skills Word Cloud')
skills_wordcloud = WordCloud(width=1000, height=500, background_color='white').generate_from_frequencies(
    {skill: count for skills_set in df['Skills'] for skill, count in pd.Series(list(skills_set)).value_counts().items()}
)
st.image(skills_wordcloud.to_array(), caption='Unique Skills Word Cloud', use_column_width=True)


st.subheader('Unique Education Word Cloud')
education_wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(
    {edu: count for education_set in df['Education'] for edu, count in pd.Series(list(education_set)).value_counts().items()}
)
st.image(education_wordcloud.to_array(), caption='Unique Education Word Cloud', use_column_width=True)
