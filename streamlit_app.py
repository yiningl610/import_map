import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("plot_data.csv")
    return data

data = load_data()

# Extract unique values
sources = sorted(data['Source'].unique())
years = sorted(data['Year'].unique())
categories = sorted(data['Category'].unique())

# Create category-to-source map
category_source_map = {}
for category in categories:
    category_source_map[category] = sorted(data[data['Category'] == category]['Source'].unique())

# Create color scales
color_scales = {}
for source in sources:
    source_data = data[data['Source'] == source]
    min_val = source_data['value'].min()
    max_val = source_data['value'].max()
    color_scales[source] = [min_val, max_val]

# Streamlit layout
st.title("U.S. Import Values Dashboard")

# Dropdowns
selected_category = st.selectbox("Select Category", categories)
selected_source = st.selectbox("Select Source", category_source_map[selected_category])

# Play/pause slider
selected_year = st.slider("Select Year", min_value=min(years), max_value=max(years), value=min(years))

# Filter data
filtered_data = data[(data['Category'] == selected_category) &
                     (data['Source'] == selected_source) &
                     (data['Year'] == selected_year)]

# Create Plotly figure
fig = go.Figure()

choropleth = go.Choropleth(
    locations=filtered_data['iso3'],
    z=filtered_data['value'],
    text=filtered_data['Country'],
    hovertemplate="<b>Country:</b> %{text}<br>" +
                  "<b>Value:</b> %{z:.2f}<br>" +
                  f"<b>Category:</b> {selected_category}<br>" +
                  f"<b>Source:</b> {selected_source}<br>" +
                  "<extra></extra>",
    colorscale='Viridis',
    zmin=color_scales[selected_source][0],
    zmax=color_scales[selected_source][1]
)

fig.add_trace(choropleth)

fig.update_layout(
    title=f"U.S. Import Values for {selected_source} in {selected_year}",
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    ),
    width=800,
    height=500
)

# Display Plotly figure
st.plotly_chart(fig, use_container_width=True)
