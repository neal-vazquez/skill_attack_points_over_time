# Skill Attack Points Over Time

## Overview
Skill Attack Points Over Time is a a visualization tool that allows Dance Dance Revolution players to visualize the trend of skill points over time. It is a Streamlit application that uses web scraping to generate a formatted line chart using an 8-digit code. On the line chart, each dot on the graph represents an update to the player's skill points on a given date, and data labels show the amount of skill points gained over the course of the calendar year.

## Features
- Scrapes data from the Skill Attack website based on a user-provided DDR code.
- Visualizes the trend of skill points over time using a line chart.
- Displays yearly gains in skill points as data labels on the chart.
- Handles edge cases such as single score submissions for a year and missing years.

## Installation
To run this application locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a virtual environment:**
   ```python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```pip install -r requirements.txt
   ```

4. **Create a virtual environment:**
   ```streamlit run sa_pts_over_time.py
   ```

## Usage

1. **Open the application:** After running the Streamlit app, a new tab will open in your default web browser.

2. **Enter the DDR code:** Enter an 8-digit DDR code without dashes in the text input field.

3. **Submit the code:** Click the "Submit" button to scrape the Skill Attack page and visualize the trend of skill points.

4. **View the chart:** The application will display a chart with skill points over time, along with yearly gains as data labels.

## Code Explanation

### `fetch_page_content(url)`

This asynchronous function fetches the page content from the given URL using `aiohttp` and decodes it using `Shift_JIS` encoding.

### `scrape_data(user_code)`

This function constructs the Skill Attack URL using the provided DDR code, fetches the page content, and parses it using `BeautifulSoup`. It extracts the username and skill point data from the JavaScript arrays embedded in the page.

### `extract_js_array(script_text, array_name)`

This function extracts JavaScript array data from the provided script text based on the array name.

### `plot_data(data, username, user_code)`

This function creates a DataFrame from the scraped data, calculates yearly points gained, and plots the data using `matplotlib`. It handles edge cases such as single score submissions for a year and missing years.

## Custom CSS

Custom CSS is applied to adjust the spacing of the title and description.

## Footer

The footer contains social media links and credits.

## Contact

For any questions or issues, please contact:

- **Author:** mio in collaboration with GPT-4o
- **Email:** [your_email@example.com]
- **GitHub:** [Your GitHub Profile](https://github.com/your_profile)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
