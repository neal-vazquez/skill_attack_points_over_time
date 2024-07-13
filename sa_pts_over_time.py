import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import aiohttp
import asyncio

async def fetch_page_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.read()
            return response_text.decode('shift_jis')  # Explicitly decode using Shift_JIS

def scrape_data(user_code):
    url = f'http://skillattack.com/sa4/dancer_skillpoint.php?ddrcode={user_code}'
    print(f'Requesting URL: {url}')

    # Fetch page content
    page_content = asyncio.run(fetch_page_content(url))

    soup = BeautifulSoup(page_content, 'html.parser')

    # Extract the username from JavaScript variable
    script = soup.find('script', text=lambda t: 'sName' in t)
    username = script.text.split("sName='")[1].split("';")[0]

    # Extract data from the JavaScript arrays
    dsUpdate = extract_js_array(script.text, 'dsUpdate')
    dsSkill = extract_js_array(script.text, 'dsSkill')

    cleaned_data = []
    for i in range(len(dsUpdate)):
        try:
            skill_point = float(dsSkill[i])
            date = dsUpdate[i]
            cleaned_data.append({'Date': date, 'Skill Point': skill_point})
            print(f'Added data: Date={date}, Skill Point={skill_point}')
        except ValueError:
            print(f'Skipping row due to invalid skill point: {dsSkill[i]}')

    return username, cleaned_data if cleaned_data else None

def extract_js_array(script_text, array_name):
    import re
    pattern = re.compile(rf"{array_name}\s*=\s*new Array\((.*?)\);", re.DOTALL)
    match = pattern.search(script_text)
    if not match:
        raise ValueError(f"Array {array_name} not found in script text")
    
    array_content = match.group(1).replace('\n', '').replace('\'', '"')
    return eval(f"[{array_content}]")

def plot_data(data, username, user_code):
    # Create DataFrame
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])

    # Calculate yearly points gained
    df['Year'] = df['Date'].dt.year
    yearly_gain = {}

    years = sorted(df['Year'].unique())
    last_year_score = None

    for i, year in enumerate(years):
        year_data = df[df['Year'] == year]
        
        if len(year_data) > 1:
            # Calculate gain as difference between last and first scores of the year
            gain = year_data['Skill Point'].iloc[-1] - year_data['Skill Point'].iloc[0]
        elif len(year_data) == 1:
            if i == 0:
                # First year with only one score
                gain = 0.0
            else:
                # Single score year, calculate gain with the last score of the previous year
                previous_year = years[i - 1]
                previous_year_data = df[df['Year'] == previous_year]
                previous_last_score = previous_year_data['Skill Point'].iloc[-1] if len(previous_year_data) > 0 else 0
                gain = year_data['Skill Point'].iloc[0] - previous_last_score

        yearly_gain[year] = gain
        last_year_score = year_data['Skill Point'].iloc[-1]

    # Handle the last year case separately if there is only one score in the last year
    if len(df[df['Year'] == years[-1]]) == 1:
        last_year = years[-1]
        if len(years) > 1:
            second_last_year = years[-2]
            last_year_score = df[df['Year'] == last_year]['Skill Point'].iloc[0]
            second_last_year_last_score = df[df['Year'] == second_last_year]['Skill Point'].iloc[-1]
            yearly_gain[last_year] = last_year_score - second_last_year_last_score
        else:
            yearly_gain[last_year] = 0.0

    # Add dash in the middle of the user code
    formatted_user_code = f"{user_code[:4]}-{user_code[4:]}"

    # Plot the data with yearly points gained as labels
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Skill Point'], marker='o', linestyle='-', color='b')

    # Add data labels for yearly points gained
    for year, gain in yearly_gain.items():
        max_date = df[df['Year'] == year]['Date'].max()
        max_skill = df[df['Year'] == year]['Skill Point'].max()
        plt.text(max_date, max_skill, f'+{abs(gain):.2f}', fontsize=9, ha='right', va='bottom')

    plt.title(f'Skill Points Over Time with Yearly Gains\nFor Player: {username} ({formatted_user_code})')
    plt.xlabel('Date')
    plt.ylabel('Skill Point')
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

st.write('''Enter an 8-digit ddr code to scrape a 
<a href="http://skillattack.com/sa4/" target="_blank">Skill Attack</a> 
page and visualize the trend of skill points for a given player over time. 
Each dot represents an update to the player's skill points on a given date 
and the data labels show the amount of skill points gained over the course of the calendar year.''', unsafe_allow_html=True)

user_code = st.text_input('Please enter the 8-digit ddr code without dashes:')

if st.button('Submit'):
    if user_code:
        username, data = scrape_data(user_code)
        if data:
            st.write('Data scraped successfully:')
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
