#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 09:39:15 2026

@author: dina.deifallah
"""

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('../data/world_happiness_2023.csv')
df.columns = ['Country','Region','Score','GDP','Social_Support',
              'Life_Expectancy','Freedom','Generosity','Corruption']

st.title("World Happiness Dashboard")

with st.sidebar:
    st.header("Filters")
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    top_n = st.slider("Show top N countries", 5, 20, 15)

filtered = df if selected_region == 'All' else df[df['Region'] == selected_region]
top = filtered.nlargest(top_n, 'Score').sort_values('Score')

# highlight colour — single bold colour draws the eye to sorted ranking
fig = px.bar(top, x='Score', y='Country', orientation='h',
             color_discrete_sequence=['#2E75B6'],  
             labels={'Score': 'Happiness Score (0–10)', 'Country': ''})

fig.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                  xaxis=dict(range=[0,8.5], gridcolor='#EEEEEE'),
                  yaxis=dict(showgrid=False),
                  font=dict(family='Arial', size=12),
                  margin=dict(l=10,r=20,t=10,b=10))

fig.update_traces(marker_line_width=0)

st.plotly_chart(fig, width='stretch')
