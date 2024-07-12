import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from requests_html import HTMLSession

def scrape_data(user_code):
    url = f'http://skillattack.com/sa4/dancer_skillpoint.php?ddrcode={user_code}'
    print(f'Requesting URL: {url}')
    
    session = HTMLSession()
    response = session.get(url)
    
    # Debugging: Show the entire HTML content
    st.write("Page content preview:", response.html.html[:1000])  # Preview the first 1000 characters of the HTML
    
    # Extract the username from JavaScript variable
    scripts = response.html.find('script', containing='sName')
    if scripts:
        username = scripts[0].text.split('sName=')[1].split(';')[0].strip("'")
    else:
        username = "Unknown"
    
    # Extract data from the table within div#score
    data = []
    score_div = response.html.find('div#score', first=True)
    
    if score_div:
        table = score_div.find('table', first=True)
        if table:
            rows = table.find('tr')[1:]  # Skip the header row
            for row in rows:
                cols = row.find('td')
                if len(cols) >= 2:
                    date = cols[0].text.strip()
                    skill_point = cols[1].text.strip()
                    try:
                        skill_point = float(skill_point)
                        data.append({'Date': date, 'Skill Point': skill_point})
                    except ValueError:
                        print(f'Skipping row due to invalid skill point: {skill_point}')
    
    if not data:
        return username, None

    return username, data

def plot_data(data, username, user_code):
    if not data:
        st.write("No data available to plot.")
        return
    
    # Create DataFrame
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])

    # Calculate yearly points gained
    df['Year'] = df['Date'].dt.year
    yearly_gain = df.groupby('Year')['Skill Point'].max().diff().fillna(0)

    # Add dash in the middle of the user code
    formatted_user_code = f"{user_code[:4]}-{user_code[4:]}"

    # Plot the data with yearly points gained as labels
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Skill Point'], marker='o', linestyle='-', color='b')

    # Add data labels for yearly points gained
    for year, gain in yearly_gain.items():
        max_date = df[df['Year'] == year]['Date'].max()
        max_skill = df[df['Year'] == year]['Skill Point'].max()
        plt.text(max_date, max_skill, f'+{gain:.2f}', fontsize=9, ha='right', va='bottom')

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
