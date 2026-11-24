#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:31:04 2026

@author: dina.deifallah
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Happiness Report", page_icon="🌐")

df = pd.read_csv('../data/world_happiness_2023.csv')

df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

st.title("World Happiness Dashboard")
st.write(f"Data loaded: {len(df)} countries")

# add a bar chart of top 15 countries in Happiness Score
top15 = df.nlargest(15, 'Score').sort_values('Score')
fig = px.bar(top15, x='Score', y='Country', orientation='h',
             labels={'Score': 'Happiness Score (0–10)', 'Country': ''},
             template='plotly_white', title="Happiest 15 Countries in 2023")

fig.update_layout(title_font=dict(family='Arial', size=13, color='slategrey'),
                  xaxis=dict(range=[0, 8.0]))


st.plotly_chart(fig, width='stretch') 