import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import os
from streamlit.components.v1 import html

# Custom CSS
st.markdown("""
<style>
    .css-z5fcl4 {
    padding: 2rem 3rem 1rem 3rem;
    }
    .css-otxysd{
        display: none;
    }
    .css-1oe5cao {
        max-height: 100vh;
    }
    .css-74h3l2{
        display: none;
    }   
</style>
""", unsafe_allow_html=True)

# Logo and text beside the logo
col1, col2 =  st.columns([0.2, 0.7])
with col1:
    # Logo Image
    logo = st.image("src/image/logo.png", width=100)
with col2:
    # Page Title
    st.title("Omdena, Kano Nigeria Chapter - Food Prices Analysis & Prediction")
st.markdown("---")# Horizontal Line below the logo

# Check if the CSV file exists, if not, create one
csv_file_path = 'src/data/feedback.csv'
if not os.path.isfile(csv_file_path):
    df = pd.DataFrame(columns=['Name', 'Email', 'Subject', 'Feedback'])
    df.to_csv(csv_file_path, index=False)

df = pd.read_csv('src/data/preprocessed_data.csv')

# Filters at the top of the page
st.title("Dashboard Filters")

col1, col2 =  st.columns(2)
with col1:
    selected_year = st.selectbox('Select Year:', df['year'].unique())
with col2:
    selected_category = st.selectbox('Select Category Type:', df['category'].unique())

# Filter the data based on user selection
filtered_df = df[(df['year'] == selected_year) & (df['category'] == selected_category)]

# Dataset
st.subheader("Filtered Data")
col1, col2 =  st.columns(2)
with col1:
    st.write(f"Selected Year: {selected_year}")
with col2:
    st.write(f"Selected Category: {selected_category}")
st.write(filtered_df)

# Chart 1: Price and Inflation Rate by Market_Name
st.subheader('Price and Inflation Rate by Market_Name')
fig1 = px.bar(filtered_df, x='Market_Name', y='price', color='Inflation')
st.plotly_chart(fig1, use_container_width=True)


# Chart 2: Price and Inflation Rate by Category
st.title(f'Inflation Rate of {selected_category} Over the Years')
yearly_inf=pd.DataFrame(df.groupby('year')['Inflation'].mean())
yearly_inf=yearly_inf.reset_index()
fig2 = px.line(yearly_inf, x=yearly_inf['year'], y=yearly_inf['Inflation'])
st.plotly_chart(fig2)

# Chart 3: Price and Inflation Rate by Year
st.subheader('Average of price by State')

# Calculate average price by state
avg_price_by_state = df.groupby('State')['price'].mean().reset_index()
# Create a Folium Map
m = folium.Map(location=[9.0820, 8.6753], zoom_start=5)

# Add Circle Markers for Average Price by State
for index, row in avg_price_by_state.iterrows():
    folium.CircleMarker(
        location=[df.loc[df['State'] == row['State'], 'latitude'].mean(), df.loc[df['State'] == row['State'], 'longitude'].mean()],
        radius=row['price'] / 100,  # Adjust the radius based on the price for better visualization
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"{row['State']} - Average Price: {row['price']:.2f}"
    ).add_to(m)

# Render the map using components
html_string = m.get_root().render()
# html(html_string)
st.components.v1.html(html_string, width=750, height=400)
