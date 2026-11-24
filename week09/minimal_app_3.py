#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:39:15 2026

@author: dina.deifallah
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Happiness Report", page_icon="🌐")

df = pd.read_csv('../data/world_happiness_2023.csv')
df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

st.title("World Happiness Dashboard 🌐")

# Add a filter for region and a filter for number of topc countries to show
with st.sidebar:
    st.header("Filters")
    regions = ['All Regions'] + sorted(df['Region'].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    top_n = st.slider("Show top N countries", 5, 20, 10)

# filter data accordingly: 
filtered = df if selected_region == 'All Regions' else df[df['Region'] == selected_region]
top = filtered.nlargest(top_n, 'Score').sort_values('Score')

# create top bar chart
fig = px.bar(top, x='Score', y='Country', orientation='h',
             labels={'Score': 'Happiness Score (0–10)', 'Country': ''},
             template='plotly_white', title=f'Happiest {top_n} Countries in 2023 - {selected_region}')

fig.update_layout(title_font=dict(family='Arial', size=13, color='slategrey'),
                  xaxis=dict(range=[0, 8.0]))


st.plotly_chart(fig, width='stretch', height=600) 