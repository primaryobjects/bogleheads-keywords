from flask import Flask, jsonify, send_from_directory
from bogleheads_scraper import get_post_titles, get_keywords
from database import get_keywords_from_database, save_keywords_to_database
from mock_db import mock
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'keywords_page.html')

@app.route('/keywords')
def get_keywords_data():
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    # Always fetch the current month's keywords
    base_url = 'https://www.bogleheads.org'
    post_titles = get_post_titles(base_url)
    current_keywords = get_keywords(post_titles)

    # Save the current month's keywords to the database
    save_keywords_to_database(current_keywords, current_year, current_month)

    # Get the previous month's keywords
    previous_month, previous_year = current_month - 1, current_year
    if previous_month == 0:
        previous_month, previous_year = 12, previous_year - 1
    previous_keywords = get_keywords_from_database(previous_year, previous_month)

    # Calculate the keyword frequency change
    keyword_changes = calculate_keyword_changes(current_keywords, previous_keywords)

    # Return the keyword changes as a JSON response
    return jsonify(keyword_changes)

def calculate_keyword_changes(current_week, previous_week):
    keyword_changes = []
    previous_week_dict = {k: (c, urls) for k, c, urls in previous_week}
    for keyword, current_count, current_urls in current_week:
        previous_count, previous_urls = previous_week_dict.get(keyword, (0, []))
        change = current_count - previous_count
        keyword_changes.append((keyword, current_count, change, current_urls))
    return keyword_changes

if __name__ == '__main__':
    mock()
    app.run(host='0.0.0.0',
    debug=True,
    port=8080)
