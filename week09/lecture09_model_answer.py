

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="World Happiness Dashboard", page_icon="🌍", layout="wide")

# ── Data ──────────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent / 'data'
df = pd.read_csv(DATA_DIR / 'world_happiness_2023.csv')

df.columns = ['Country', 'Region', 'Score', 'GDP', 'Social_Support',
              'Life_Expectancy', 'Freedom', 'Generosity', 'Corruption']

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.selectbox("Region", regions)
    top_n = st.slider("Show top N countries", 5, 30, 15)


# ── Filtered data ─────────────────────────────────────────────────────────────
filtered = df if selected_region == 'All' else df[df['Region'] == selected_region]
top = filtered.nlargest(top_n, 'Score').sort_values('Score')

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🌍 World Happiness Dashboard")
st.caption("Source: World Happiness Report 2023 | Kaggle")

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)
k1.metric("Countries", len(filtered))
k2.metric("Avg Happiness Score", f"{filtered['Score'].mean():.2f}",
          f"{filtered['Score'].mean() - df['Score'].mean():+.2f} vs global")
k3.metric("Happiest in selection",
          filtered.nlargest(1, 'Score')['Country'].values[0],
          f"Score: {filtered['Score'].max():.2f}")

st.divider()

# ── Row 1: Rankings + Scatter ─────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Happiness Rankings")
    # BBD COLOUR TYPE: sequential — ordered bars, one direction (light→dark)
    fig1 = px.bar(
        top, x='Score', y='Country', orientation='h',
        color='Score',
        color_continuous_scale='Blues',
        range_color=[4.5, 8.5],
        labels={'Score': 'Happiness Score (0–10)', 'Country': ''},
    )
    fig1.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(range=[0, 8.5], gridcolor='#EEEEEE'),
        yaxis=dict(showgrid=False),
        coloraxis_showscale=False,
        font=dict(family='Arial', size=12),
        margin=dict(l=10, r=10, t=5, b=10),
    )
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Score vs GDP")
    # BBD COLOUR TYPE: highlight — single colour, focus on the pattern
    fig2 = px.scatter(
        filtered, x='GDP', y='Score', hover_name='Country',
        color_discrete_sequence=['#2E75B6'],
        labels={'GDP': 'Log GDP per Capita', 'Score': 'Happiness Score'},
    )
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(gridcolor='#EEEEEE'),
        yaxis=dict(gridcolor='#EEEEEE'),
        font=dict(family='Arial', size=12),
        margin=dict(l=10, r=10, t=5, b=10),
    )
    fig2.update_traces(marker=dict(size=9, opacity=0.8))
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Factor breakdown ───────────────────────────────────────────────────
st.subheader("Factor breakdown for top countries")

factors = ['GDP', 'Social_Support', 'Life_Expectancy', 'Freedom']
top10 = filtered.nlargest(10, 'Score')

# BBD COLOUR TYPE: categorical — each factor is an unordered distinct category
fig3 = px.bar(
    top10.melt(id_vars='Country', value_vars=factors),
    x='value', y='Country', color='variable', orientation='h',
    barmode='stack',
    # BBD CVD: no red-green; blue-green-yellow-grey palette
    color_discrete_sequence=['#2E75B6', '#70AD47', '#FFC000', '#AAAAAA'],
    labels={'value': 'Contribution', 'variable': 'Factor', 'Country': ''},
)
fig3.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(family='Arial', size=12),
    xaxis=dict(gridcolor='#EEEEEE'),
    legend=dict(orientation='h', y=1.2),
    margin=dict(l=10, r=10, t=40, b=10),
)
fig3.update_traces(marker_line_width=0)
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.caption("Built with Streamlit + Plotly")