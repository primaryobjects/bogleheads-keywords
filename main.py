from flask import Flask, jsonify, send_from_directory, send_file
from flask_caching import Cache
from bogleheads_scraper import get_post_titles, get_keywords
from database import get_keywords_from_database, save_keywords_to_database
from mock_db import mock
import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/css/style.css')
def css():
    return send_from_directory('css', 'style.css')

@app.route('/scripts/script.js')
def script():
    return send_from_directory('scripts', 'script.js')

@app.route('/')
def index():
    return send_from_directory('.', 'keywords_page.html')

@app.route('/keywords')
@cache.cached(timeout=300)  # cache this view for 5 minutes
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
    return jsonify({
        'data': keyword_changes,
        'cache_datetime': datetime.datetime.now().isoformat()
    })

@app.route('/wordcloud.png')
@cache.cached(timeout=300)  # cache this view for 5 minutes
def generate_wordcloud():
    # Get the keyword data
    keyword_data = get_keywords_data().json['data']
    # Create a dictionary of keyword frequencies
    frequencies = {keyword: count for keyword, count, _, _ in keyword_data}
    # Generate the word cloud
    wc = WordCloud(width=800, height=400, background_color='white')
    wc.generate_from_frequencies(frequencies)
    # Save the word cloud to a PNG image
    img = io.BytesIO()
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return send_file(img, mimetype='image/png')

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
