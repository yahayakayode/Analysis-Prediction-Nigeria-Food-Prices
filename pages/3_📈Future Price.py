import streamlit as st
import pandas as pd
import pickle
import datetime as dt
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Set Page Configuration for a Wider Layout
st.set_page_config(layout="wide")
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


parent_directory = Path(__file__).resolve().parent.parent

# Correctly join the path to your model
model_path = os.path.join(parent_directory, "src/model/abhinash_model.pkl")
encoded_features_path = os.path.join(parent_directory, "src/model/encoded_dict.pkl")

with open(model_path, "rb") as file:
    model = pickle.load(file)

with open(encoded_features_path, "rb") as file:
    encoded_features = pickle.load(file)

if "predictions" not in st.session_state:
    st.session_state["predictions"] = []

market_locations = pd.DataFrame.from_dict(encoded_features["markets_dict"]).T.rename(
    columns={"latitude": "lat", "longitude": "lon"}
)


def make_prediction(date, product, pricetype, market):
    # latitute and longitude
    latitude = encoded_features["markets_dict"][market]["latitude"]
    longitude = encoded_features["markets_dict"][market]["longitude"]

    # sin cos the month
    year = date.year
    month_categorical = date.month
    sin_month = np.sin(2 * np.pi * month_categorical / 12)
    cos_month = np.cos(2 * np.pi * month_categorical / 12)

    # encode the food item
    commodities_categorical = encoded_features["food_item_mapping"][product]

    season_categorical = encoded_features["season_dict"][
        encoded_features["season_dict_months"][str(month_categorical)]
    ]
    commodities_categorical = encoded_features["category_dict"][
        encoded_features["category_commodity_dict"][product]
    ]

    columns = [
        "latitude",
        "longitude",
        "year",
        "season_categorical",
        "pricetype_binary",
        "month_categorical",
        "commodities_categorical",
        "month_sin",
        "month_cos",
    ]

    input_df = pd.DataFrame(
        [
            [
                latitude,
                longitude,
                year,
                season_categorical,
                pricetype,
                month_categorical,
                commodities_categorical,
                sin_month,
                cos_month,
            ]
        ],
        columns=columns,
    )
    prediction = model.predict(input_df)

    return round(prediction[0], 2)


st.title("Future Price Prediction")

# Date input
selected_date = st.date_input("Select a date", dt.datetime.today())

# Product selection
product_list = encoded_features["food_item_mapping"].keys()
selected_product = st.selectbox("Select a Product", product_list, index=0)

# select the market
market_list = encoded_features["markets_dict"].keys()
selected_market = st.selectbox("Select a Market", market_list, index=0)

# Price Type selection
price_type_list = ["Retail", "Wholesale"]
selected_price_type = st.selectbox("Select a Price Type", price_type_list)
pricetype_binary = encoded_features["pricetype_dict"][selected_price_type]
st.markdown("""<br>""", unsafe_allow_html=True)

left_column, central_column, right_column = st.columns([1, 2, 1])

with central_column:
    if st.button("Predict Price", use_container_width=True):
        result = make_prediction(
            selected_date, selected_product, pricetype_binary, selected_market
        )

        st.write(f"The predicted price for {selected_product} on {selected_date} is:")
        st.title(f"{result} Naira")

        new_prediction = {
            "Date": selected_date,
            "Product": selected_product,
            "Market": selected_market,
            "Price Type": selected_price_type,
            "Predicted Price": result,
        }
        st.session_state.predictions.insert(0, new_prediction)

if len(st.session_state.predictions) > 0:
    st.markdown("""<br>""", unsafe_allow_html=True)
    st.write("Recent Predictions:")
    st.table(pd.DataFrame(st.session_state.predictions))
