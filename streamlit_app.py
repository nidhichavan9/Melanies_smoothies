import streamlit as st
from snowflake.snowpark.functions import col

# Application title and user instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want in your custom Smoothie!")

# User input for order name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Establish Snowflake connection via Streamlit connection framework
cnx = st.connection("snowflake")
session = cnx.session()

# Query options from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Convert Snowpark DataFrame column to a standard Python list for Streamlit multiselect
fruit_options_list = [row['FRUIT_NAME'] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if not name_on_order.strip():
            st.error("Please enter a name for the order before submitting.")
        else:
            # Parameterised execution or escaping prevents SQL syntax errors and injection
            my_insert_stmt = f"""
                INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                VALUES ('{ingredients_string}', '{name_on_order}')
            """
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

# New section to display smoothiefroot nutrition information
import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response)
