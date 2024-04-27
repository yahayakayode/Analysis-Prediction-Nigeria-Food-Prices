import streamlit as st
import pandas as pd
import os

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

# Streamlit App
st.title("📨User Community and Feedback!")

# Input Form
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name:")
with col2:
    email = st.text_input("Email:")
subject = st.text_input("Subject:")
feedback = st.text_area("Feedback:")
if st.button("Submit"):
    if name and email and subject and feedback:
        # Load existing data from CSV
        df = pd.read_csv(csv_file_path)
        
        # Append new entry
        new_entry = {'Name': name, 'Email': email, 'Subject': subject, 'Feedback': feedback}
        # df = df.append(new_entry, ignore_index=True)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Save updated data to CSV
        df.to_csv(csv_file_path, index=False)
        
        st.success("Thank you for the feedback!")
    else:
        st.warning("Please fill out all fields.")


st.subheader("Visit Dagshub Repository")
st.markdown("[Dagshub](https://dagshub.com/Omdena/KanoNigeriaChapter_FoodPrices)", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.write("© 2023. Developed with 💚 by Omdena Nigeria Chapter.")