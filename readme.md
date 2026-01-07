# 🍽️ Restaurant Review Dashboard

**An End-to-End System for Scraping and Analyzing Restaurant Reviews**

---

## ✨ Project Overview

This project is a complete restaurant review scraping and analysis system built with **Python**, **Selenium**, and **Streamlit**. It scrapes 1,800+ customer reviews from **OpenTable** restaurant pages, processes them, and presents insights through an interactive dashboard featuring:

- Review exploration with filters and search  
- Sentiment-highlighted food & service analysis  
- Rating trend charts and automated review summaries  
- Competitor comparison via live scraping  

---

## 🎯 Objectives

- Scrape large-scale, real-world restaurant reviews  
- Handle dynamic web pages and pagination using Selenium  
- Store and process reviews in JSON format  
- Visualize trends and insights interactively  
- Enable comparison between multiple restaurants  

---

## 🛠️ Technologies Used

- **Python** – Core programming language  
- **Streamlit** – Interactive web dashboard  
- **Selenium** – Dynamic web scraping  
- **BeautifulSoup concepts** – Parsing HTML  
- **Pandas** – Data processing and analysis  
- **Matplotlib** – Visualization  
- **WebDriver Manager** – Automated driver management  
- **JSON** – Data storage  

---

## 📦 Project Folder

- `app.py` – streamlit file
- `project.ipynb` – main project file
- `requirements.txt` – requirements txt
- `README.md` – readme

---

## ⚙️ Features

### 🔹 1. Live Review Scraping
- Scrapes reviews directly from OpenTable restaurant URLs  
- Extracts:  
  - Restaurant name  
  - Customer name  
  - Review text  
  - Rating (stars)  
  - Review date  
- Automatically navigates multiple pages  

### 🔹 2. Review Exploration
- Filter reviews by rating  
- Search reviews by customer name  
- Expandable review cards  
- Star-based rating display ⭐  

### 🔹 3. Rating & Trend Analysis
- Visualize average ratings over time  
- Compare multiple restaurants  
- Generate summary insights automatically  

---

## 🚀 How to Run the Project

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-username/restaurant-review-dashboard.git
cd restaurant-review-dashboard
   ```

2️⃣ **Run the Streamlit App**
streamlit run app.py

## ⚠️ Ethical Considerations

- Scraping performed **for educational and academic purposes only**  
- **No personal or sensitive user data** was collected  
- Pagination delays were added to avoid server overload  
- Website access policies were respected  

---

## 🔮 Future Improvements

- Implement NLP-based **sentiment classification model**  
- Perform **topic modeling (LDA)** on reviews   
- Deploy on **Streamlit Cloud**  
- Integrate a **database** (MongoDB / PostgreSQL)  

---

## © Copyright Notice

© 2026 Minahil Rizwan. All rights reserved.  

This project, including source code, design, data processing logic, and documentation, is the intellectual property of **Minahil Rizwan**.  
No part of this project may be copied, modified, distributed, or used for commercial or academic purposes without prior written permission.


This project, including its source code, design, data processing logic, and documentation, is the intellectual property of Minahil Rizwan.

No part of this project may be copied, modified, distributed, or used for commercial or academic purposes without prior written permission from the author.
