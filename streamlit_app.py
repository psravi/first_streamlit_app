
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    try 
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
    except as e:
        streamlit.error()
    
# New section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please slect a fruit to get information.")
    else:
        #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)  # output as a table
except URLError as e:
    streamlit.error()
    
#option = streamlit.selectbox('What fruit would you like information about?',  ('Watermelon','Banana','Orange','Raspberry'))
#streamlit.write('The user entered ', option)
#streamlit.text(fruityvice_response.json())
#take the json of the response and normalize it


#don't run anything past here while we troubleshoot.
streamlit.stop()

# SNOWFLAKE Connector and querying
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Snowflake Details:")
streamlit.text(my_data_row)
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit load list contains:")
streamlit.dataframe(my_data_rows)
add_my_fruit = streamlit.text_input('Add new fruit to Snowflake DB Table?','Jackfruit')
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('from streamlit')")
streamlit.write('Thanks for adding ',add_my_fruit) 
