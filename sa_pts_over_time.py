import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import re

def scrape_data(user_code):
    url = f"http://skillattack.com/sa4/dancer_skillpoint.php?ddrcode={user_code}"
    response = requests.get(url)
    page_content = response.text

    # Extract JavaScript variables
    dddIndex = extract_js_array(page_content, 'dddIndex')
    ddsMusic = extract_js_array(page_content, 'ddsMusic')
    dddStyle = extract_js_array(page_content, 'dddStyle')
    dddSequence = extract_js_array(page_content, 'dddSequence')
    dddDifficulty = extract_js_array(page_content, 'dddDifficulty')
    ddsScore = extract_js_array(page_content, 'ddsScore')
    dddFc = extract_js_array(page_content, 'dddFc')
    ddsPoint = extract_js_array(page_content, 'ddsPoint')

    # Combine data into a structured format
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

    # Extract the username from JavaScript variable
    username = extract_js_variable(page_content, 'sName')

    return username, data

def extract_js_array(content, var_name):
    regex = re.compile(rf"{var_name}\s*=\s*new Array\(\);(.*?)\s*;", re.DOTALL)
    match = regex.search(content)
    if match:
        array_content = match.group(1).strip()
        array_content = array_content.replace('new Array(', '[').replace(')', ']')
        array_content = re.sub(r'\s+', '', array_content)
        return eval(array_content)
    return []

def extract_js_variable(content, var_name):
    regex = re.compile(rf"{var_name}\s*=\s*'(.*?)';")
    match = regex.search(content)
    if match:
        return match.group(1)
    return None

def plot_data(data, username, user_code):
    df = pd.DataFrame(data)
    st.write(f"Skill Attack Points Over Time for {username} (Code: {user_code})")
    st.write(df)

    plt.figure(figsize=(10, 5))
    plt.plot(df['Index'], df['Point'], marker='o')
    plt.title(f"Skill Attack Points Over Time for {username}")
    plt.xlabel('Index')
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
