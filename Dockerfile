# Use the official Python image with Node.js pre-installed
FROM mcr.microsoft.com/playwright:focal

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN npx playwright install --with-deps

# Expose the Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "sa_pts_over_time.py"]
