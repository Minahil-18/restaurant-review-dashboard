📌 Project Overview

This project is an end-to-end restaurant review scraping and analysis system built using Python, Selenium, and Streamlit.

It scrapes 1800+ customer reviews from restaurant pages on OpenTable, processes them, and presents insights through an interactive dashboard featuring:

Review exploration

Sentiment-highlighted food & service analysis

Rating trend charts

Automated review summaries

Competitor comparison via live scraping

🎯 Objectives

Scrape large-scale real-world restaurant reviews

Handle dynamic web pages and pagination using Selenium

Store and process reviews in JSON format

Visualize trends and insights interactively

Enable comparison between multiple restaurants

🛠️ Technologies Used

Python

Streamlit – Interactive dashboard

Selenium – Dynamic web scraping

BeautifulSoup concepts

Pandas – Data processing

Matplotlib – Visualization

WebDriver Manager

JSON – Data storage

📂 Project Structure
📁 project-folder
│
├── app.py                  # Main Streamlit application
├── project.ipynb
├── requirements.txt
└── README.md

⚙️ Features
🔹 1. Live Review Scraping

Scrapes reviews directly from OpenTable restaurant URLs

Extracts:

Restaurant name

Customer name

Review text

Rating (stars)

Review date

Automatically navigates multiple pages

🔹 2. Review Exploration

Filter reviews by rating

Search reviews by customer name

Expandable review cards

Star-based rating display ⭐


🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/your-username/restaurant-review-dashboard.git
cd restaurant-review-dashboard

2️⃣ Run the Streamlit App
streamlit run app.py

⚠️ Ethical Considerations

Scraping performed for educational and academic purposes only

No personal or sensitive user data was collected

Pagination delays were added to avoid server overload

Website access policies were respected

🔮 Future Improvements

NLP-based sentiment classification model

Topic modeling (LDA)

Recommendation system

Deployment on Streamlit Cloud

Database integration (MongoDB / PostgreSQL)

© Copyright Notice

© 2026 Minahil Rizwan. All rights reserved.

This project, including its source code, design, data processing logic, and documentation, is the intellectual property of Minahil Rizwan.
No part of this project may be copied, modified, distributed, or used for commercial or academic purposes without prior written permission from the author.