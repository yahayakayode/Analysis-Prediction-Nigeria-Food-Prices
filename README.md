# Kano Nigeria Chapter Food Prices Analysis

This project leverages Machine Learning techniques and Python programming to analyze historical food prices data in Nigeria, predict future prices, and offer valuable insights for consumers, policymakers, and stakeholders.

## Getting Started

### Prerequisites

- Python (3.6 or later)

### Installation

1. Clone the repository:

   ```bash
   git clone https://dagshub.com/Omdena/KanoNigeriaChapter_FoodPrices.git



2. To install the required dependencies, run the following command in your terminal:

    ```
    pip install streamlit



## Running the Application

Ensure you are in the project directory, then execute the following command to run the Streamlit application:

```bash
streamlit run 1 (after typing 1 press 'Tab' button on keyboard to auto-fill the name of file as it uses emoji in the filename)
```

## Customizing Themes and CSS

If you want to customize the theme or apply custom CSS:

1. Open the `.streamlit/config.toml` file.

2. Modify the theme settings and add custom CSS:

    ```toml
    [theme]
    base="dark"
    primaryColor="#f1df10"
    backgroundColor="#014803"
    secondaryBackgroundColor="#318100"
    textColor="#ffffff"
    font="serif"
    

3. To apply additional CSS, you can inject it directly into your Streamlit Python script using the `st.markdown` function:

    ```python
    st.markdown("""
        <style>
            /* Your custom CSS styles here */
        </style>
    """, unsafe_allow_html=True)

## Explore the Application

Open your web browser and go to [http://localhost:8501](http://localhost:8501) to explore the different sections of the app. This web address works after you run the file using "streamlit run file_name.py"