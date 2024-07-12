import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from requests_html import HTMLSession
import re

def scrape_data(user_code):
    session = HTMLSession()
    url = f'http://skillattack.com/sa4/dancer_skillpoint.php?ddrcode={user_code}'
    response = session.get(url)
    
    # Render JavaScript
    response.html.render()
    
    # Extract JavaScript arrays from the page content
    page_content = response.html.html
    
    # Finding the JavaScript arrays in the page content
    dddIndex = find_js_array(page_content, 'dddIndex')
    ddsMusic = find_js_array(page_content, 'ddsMusic')
    dddStyle = find_js_array(page_content, 'dddStyle')
    dddSequence = find_js_array(page_content, 'dddSequence')
    dddDifficulty = find_js_array(page_content, 'dddDifficulty')
    ddsScore = find_js_array(page_content, 'ddsScore')
    dddFc = find_js_array(page_content, 'dddFc')
    ddsPoint = find_js_array(page_content, 'ddsPoint')
    
    # Assuming all arrays have the same length
    data = []
    for i in range(len(dddIndex)):
        for j in range(len(dddIndex[i])):
            data.append({
                "Index": dddIndex[i][j],
                "Music": ddsMusic[i][j],
                "Style": dddStyle[i][j],
                "Sequence": dddSequence[i][j],
                "Difficulty": dddDifficulty[i][j],
                "Score": ddsScore[i][j],
                "Fc": dddFc[i][j],
                "Point": ddsPoint[i][j]
            })
    
    return data

def find_js_array(page_content, array_name):
    start = page_content.find(f"{array_name} = new Array();")
    end = page_content.find(";", start)
    array_content = page_content[start:end]
    return eval(array_content.replace("new Array", ""))

def plot_data(data, username, user_code):
    df = pd.DataFrame(data)
    st.write(f"Skill Attack Points Over Time for {username} (Code: {user_code})")
    st.write(df)

    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Point'], marker='o')
    plt.title(f"Skill Attack Points Over Time for {username}")
    plt.xlabel('Date')
    plt.ylabel('Points')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

st.set_page_config(page_title="Skill Attack Points Over Time", page_icon=":chart_with_upwards_trend:")

# Custom CSS to adjust spacing
custom_css = """
<style>
h1 {
    margin-bottom: 1px;  /* Reduce space between title lines */
}
.title-section {
    margin-bottom: 30px;  /* Increase space below the title */
}
</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title-section"><h1>Skill Attack Points Over Time<br>Chart Generator</h1>', unsafe_allow_html=True)

st.write("Enter the 8-digit ddr code to scrape a Skill Attack page and visualize the trend of skill points for a given user over time. Each dot represents an update to the player's skill points on a given date and the data labels show the amount of skill points gained over the course of the calendar year.")
st.markdown('<div class="title-section"><br>', unsafe_allow_html=True)

user_code = st.text_input('Please enter the 8-digit ddr code:')

if st.button('Submit'):
    if user_code:
        username, data = scrape_data(user_code)
        if data:
            st.write('Data scraped successfully:')
            st.write(data)
            plot_data(data, username, user_code)
        else:
            st.write('No data found or invalid user code.')
    else:
        st.write('Please enter a valid 8-digit code.')

# Footer with social media links
footer = """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    padding: 10px 0;
}
.footer a {
    color: #4CAF50;
    text-decoration: none;
    padding: 0 10px;
}
.footer a:hover {
    text-decoration: underline;
}
</style>
<div class="footer">
    <p>Written by mio in collab with GPT-4o</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
