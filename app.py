import streamlit as st
import json
import base64
import time
import logging
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return []

def display_stars(rating_text):
    try:
        rating = int(rating_text.split()[0]) 
        return "⭐" * rating
    except:
        return "No Rating"

def highlight_text(text, sentiment, category):
    sentiment_color = "peachpuff" if sentiment.lower() in ["positive", "negative"] else "gray"
    if category == "food":
        return f"<span style='color: indianred; font-weight: bold'>{text}</span><br><span style='color: white; font-weight: bold;'>Sentiment: <span style='color: {sentiment_color};'>{sentiment}</span></span>"
    elif category == "service":
        return f"<span style='color: teal; font-weight: bold'>{text}</span><br><span style='color: white; font-weight: bold;'>Sentiment: <span style='color: {sentiment_color};'>{sentiment}</span></span>"
    return text

def add_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
st.markdown(
    """
    <style>
    /* Sidebar container with gradient background */
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(135deg, #2b2d42, #8d99ae);
        border-radius: 10px;
        padding: 20px;
        color: white;
    }

    /* Sidebar text elements */
    [data-testid="stSidebar"] label {
        font-size: 16px;
        color: white;
        font-weight: bold;
    }

    /* Sidebar radio buttons with hover effect */
    [data-testid="stSidebar"] .st-radio div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        padding: 8px;
        margin-bottom: 5px;
        color: white;
        transition: background 0.3s;
    }

    [data-testid="stSidebar"] .st-radio div:hover {
        background: rgba(255, 255, 255, 0.3);
    }

    /* Styled selectbox */
    [data-testid="stSidebar"] .stSelectbox {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        color: white;
        padding: 5px;
    }

    /* Input fields */
    [data-testid="stSidebar"] .stTextInput {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        color: white;
        padding: 8px;
    }

    /* Header styling */
    [data-testid="stSidebar"] h3 {
        font-size: 20px;
        color: white;
        text-align: left;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)



background_image = "ele.jpg"

def overall(df, restaurant_name):
    df['rating_value'] = df['rating'].apply(lambda x: int(x.split()[0]))
    
    avg_rating = df['rating_value'].mean()
    total_reviews = len(df)
    positive_reviews = df[df['rating'] == '5 stars'].shape[0]
    negative_reviews = df[df['rating'] == '1 star'].shape[0]
    
    # Latest review
    latest_review = df.loc[df['review_date'].idxmax()]
    latest_review_content = latest_review['review_content']
    latest_review_date = latest_review['review_date']

    summary = f"""
    Overall Review Summary for {restaurant_name}:
    - Average Rating: {avg_rating:.2f} stars
    - Total Reviews: {total_reviews}
    - Positive Reviews (5 stars): {positive_reviews}
    - Negative Reviews (1 star): {negative_reviews}
    
    Latest Review:
    - Date: {latest_review_date}
    - Review: {latest_review_content}

    """
    return summary

def convert_date(date_str):
    if 'days ago' in date_str:
        days_ago = int(date_str.split()[1])
        return datetime.now() - timedelta(days=days_ago)
    elif 'Dined on' in date_str:
        return pd.to_datetime(date_str.replace('Dined on ', ''), format='%B %d, %Y')
    elif 'Dined today' in date_str:
        return datetime.now()
    else:
        return pd.to_datetime(date_str, format="%Y-%m-%d", errors='coerce')
        
def scrape_opentable_reviews(url):
    try:
        logging.basicConfig(level=logging.DEBUG)
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        except Exception as e:
            logging.error(f"Error initializing ChromeDriver: {e}")
            st.error(f"Error initializing ChromeDriver: {e}")
            return []

        driver.get(url)
        time.sleep(3) 

        data = []
      
        try:
            restaurant_name = driver.find_element(By.CLASS_NAME, 'E-vwXONV9nc-').text
            logging.info(f"Restaurant Name: {restaurant_name}")
        except Exception as e:
            logging.error(f"Error extracting restaurant name: {e}")
            st.error("Error extracting restaurant name.")
            driver.quit()
            return []

        while True:
            try:
                names = driver.find_elements(By.CLASS_NAME, '_0Uufw15R3a4-')
                customer_names = [name.find_element(By.CLASS_NAME, '_1p30XHjz2rI-').text for name in names if name.text]

                items = driver.find_elements(By.CLASS_NAME, 'MpiILQAMSSg-')
                for i in range(len(items)):
                    try:
                        content = items[i].find_element(By.CLASS_NAME, '_6rFG6U7PA6M-')
                        date = items[i].find_element(By.CLASS_NAME, 'iLkEeQbexGs-')
                        rating_element = items[i].find_element(By.CLASS_NAME, 'yEKDnyk-7-g-')
                        rating = rating_element.get_attribute("aria-label")
                        
                        customer_name = customer_names[i] if i < len(customer_names) else None
                        
                        data.append({
                            "restaurant_name": restaurant_name,
                            "customer_name": customer_name,
                            "review_content": content.text,
                            "rating": rating,
                            "review_date": date.text
                        })
                    except Exception as e:
                        logging.error(f"Error processing review item: {e}")

                logging.info("Page Loaded - Collecting data...")

                # Check for the Next button and navigate if available
                footer = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, '_1BEc9Aeng-Q-'))
                )
                buttons = footer.find_elements(By.CLASS_NAME, 'TkpxbcBbu80-')
                
                if len(buttons) > 1:
                    next_button = buttons[1]
                else:
                    next_button = buttons[0]

                if "disabled" in next_button.get_attribute("class") or not next_button.is_displayed():
                    logging.info("No more pages to load.")
                    break 

                next_button.click()
                logging.info("Navigating to the next page...")
                time.sleep(3)
            
            except Exception as e:
                logging.error(f"Error navigating to the next page: {e}")
                break

        driver.quit() 
        return data
    
    except Exception as e:
        logging.error(f"Error while scraping reviews: {e}")
        st.error(f"Error while scraping reviews: {e}")
        return []


processed_reviews = load_json_data("final_reviews.json")
original_reviews = load_json_data("reviews.json")
add_background(background_image)

st.title("Minah's Dashboard")

option = st.sidebar.radio("Choose an Option", ["Reviews", "Charts", "Review Summary"])

if option == "Reviews":
    competitor_url = st.text_input("Enter OpenTable link for competitor restaurant:")
    if st.button("Scrape and Compare Ratings"):
        st.info("Starting data scraping...")
        competitor_reviews = scrape_opentable_reviews(competitor_url)
        if competitor_reviews:
            st.success(f"Scraped {len(competitor_reviews)} reviews!")
            for review in competitor_reviews:
                with st.expander(f"Review by {review['customer_name']}"):
                    st.write(f"*Review Date:* {review['review_date']}")
                    st.write(f"*Rating:* {display_stars(review['rating'])}")
                    st.markdown(f"*Review Content:* {review['review_content']}")

    st.sidebar.header("Filter Reviews")
    filter_rating = st.sidebar.selectbox("Filter by Rating:", ["All", "5 stars", "4 stars", "3 stars", "2 stars", "1 star"])
    search_customer = st.sidebar.text_input("Search by Customer Name:")

    for original, processed in zip(original_reviews, processed_reviews):
        customer_name = original.get("customer_name", "Unknown Customer")
        review_content = original.get("review_content", "No review content available")
        rating = original.get("rating", "No Rating")
        stars = display_stars(rating)
        review_date = original.get("review_date", "No Date")
        food_quality = processed.get("food_quality", {"comment": "No Food Review", "sentiment": "Neutral"})
        staff_service = processed.get("staff_service", {"comment": "No Service Review", "sentiment": "Neutral"})

        if filter_rating != "All" and filter_rating != rating:
            continue
        if search_customer and search_customer.lower() not in customer_name.lower():
            continue

        with st.expander(f"Review by {customer_name}"):
            st.write(f"*Review Date:* {review_date}")
            st.write(f"*Rating:* {stars}")
            st.markdown(f"*Review Content:* {review_content}")
            st.markdown(f"<br><b>Food Quality:</b> {highlight_text(food_quality['comment'], food_quality['sentiment'], 'food')}", unsafe_allow_html=True)
            st.markdown(f"<br><b>Staff Service:</b> {highlight_text(staff_service['comment'], staff_service['sentiment'], 'service')}", unsafe_allow_html=True)



elif option == "Charts":
    df1 = pd.read_json('reviews.json')  
    df2 = pd.read_json('second.json') 

    df1['review_date'] = df1["review_date"].apply(convert_date)
    df2['review_date'] = df2["review_date"].apply(convert_date)

    ratings1 = df1["rating"].apply(lambda x: int(x.split()[0]))
    ratings2 = df2["rating"].apply(lambda x: int(x.split()[0]))

    sample1 = pd.DataFrame({'Date': df1['review_date'], 'Rating': ratings1})
    sample2 = pd.DataFrame({'Date': df2['review_date'], 'Rating': ratings2})

    yearly1 = sample1.resample('YE', on='Date').mean()
    yearly2 = sample2.resample('YE', on='Date').mean()

    ranges = [(2005, 2008), (2009, 2012), (2013, 2016), (2017, 2020), (2021, 2024)]

    def filter_range(df, r):
        filtered = []
        for start_year, end_year in r:
            filtered.append(df[(df.index.year >= start_year) & (df.index.year <= end_year)])
        return pd.concat(filtered)

    filtered1 = filter_range(yearly1, ranges)
    filtered2 = filter_range(yearly2, ranges)

    st.subheader('Rating Trends for Each Restaurant')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 16))

    # Plot for Restaurant 1
    ax1.plot(filtered1.index, filtered1['Rating'], label='Restaurant 1', color='navy', marker='o', linestyle='-', linewidth=2)
    ax1.set_title('Rating Trends for Restaurant 1')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Average Rating')
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax1.grid(True)

    # Plot for Restaurant 2
    ax2.plot(filtered2.index, filtered2['Rating'], label='Restaurant 2', color='teal', marker='x', linestyle='--', linewidth=2)
    ax2.set_title('Rating Trends for Restaurant 2')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Average Rating')
    ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax2.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader('Comparison of Rating Trends Between Restaurants')

    fig, ax = plt.subplots(figsize=(14, 8))

    for start_year, end_year in ranges:
        range1 = yearly1[(yearly1.index.year >= start_year) & (yearly1.index.year <= end_year)]
        range2 = yearly2[(yearly2.index.year >= start_year) & (yearly2.index.year <= end_year)]

        ax.plot(range1.index, range1['Rating'], label=f'Restaurant 1 ({start_year}-{end_year})', color='teal', marker='o', linestyle='-', linewidth=3, markersize=8)
        ax.plot(range2.index, range2['Rating'], label=f'Restaurant 2 ({start_year}-{end_year})', color='mediumvioletred', marker='x', linestyle='--', linewidth=3, markersize=8)

    ax.set_title('Rating Comparison Trends for Restaurant 1 & Restaurant 2', fontsize=20, fontweight='bold', color='darkslategray', fontname='Times New Roman')
    ax.set_xlabel('Year', fontsize=14, fontweight='light', color='dimgray', labelpad=15)
    ax.set_ylabel('Average Rating', fontsize=14, fontweight='light', color='dimgray', labelpad=15)

    plt.xticks(rotation=45, fontsize=12, color='slategray', fontweight='medium')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Restaurant & Year Range', title_fontsize=13, fontsize=12, frameon=True, framealpha=0.7, fancybox=True, facecolor='whitesmoke')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    st.pyplot(fig)


elif option == "Review Summary":
    
    df1 = pd.read_json('reviews.json') 
    df2 = pd.read_json('second.json')  
    restaurants_1 = df1['restaurant_name'].unique()
    
    for restaurant in restaurants_1:
        restaurant_df_1 = df1[df1['restaurant_name'] == restaurant]
        summary_1 = overall(restaurant_df_1, restaurant)
        st.markdown(f"### {restaurant}")
        st.markdown(summary_1)
    
    restaurants_2 = df2['restaurant_name'].unique()
    
    for restaurant in restaurants_2:
        restaurant_df_2 = df2[df2['restaurant_name'] == restaurant]
        summary_2 = overall(restaurant_df_2, restaurant)
        st.markdown(f"### {restaurant}")
        st.markdown(summary_2)

st.markdown("---")
st.markdown("### - by Minahil Rizwan")
