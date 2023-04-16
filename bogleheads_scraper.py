import requests
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import re
from nltk import bigrams, trigrams
import nltk
import datetime

nltk.download('stopwords')

def get_post_titles(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles_with_urls = []
    for tr in soup.find('table', {'id': 'posts_table'}).find_all('tr', {'style': 'vertical-align:baseline;'}):
        td = tr.find_all('td')[2]
        a = td.find('a')
        if a is not None:
            title = a.get_text()
            url = a['href']
            titles_with_urls.append((title, url))
    return titles_with_urls

def get_keywords(titles_with_urls):
    stopwords = nltk.corpus.stopwords.words('english')
    keyword_dict = defaultdict(list)

    for title, url in titles_with_urls:
        # Remove all non-letter characters from the title
        title = re.sub(r'[^a-zA-Z\s]', '', title)
        # Convert the title to lowercase
        title = title.lower()
        # Split the title into a list of words
        words = title.split()
        # Remove stopwords and numbers from the list of words
        words = [word for word in words if word not in stopwords and not word.isnumeric()]

        # Create trigrams from the list of words
        trigram_list = list(trigrams(words))
        # Add the trigrams and their associated URLs to the keyword dictionary
        for trigram in trigram_list:
            keyword_dict[' '.join(trigram)].append(url)

        # Create bigrams from the list of words
        bigram_list = list(bigrams(words))
        # Add the bigrams and their associated URLs to the keyword dictionary
        for bigram in bigram_list:
            keyword_dict[' '.join(bigram)].append(url)

        # Add the unigrams (words) and their associated URLs to the keyword dictionary
        for word in words:
            keyword_dict[word].append(url)

    # Count the frequency of each keyword
    keyword_counts = {k: len(v) for k, v in keyword_dict.items()}

    # Filter trigrams and bigrams with frequency >= 1 and combine with unigrams
    filtered_keywords = {k: v for k, v in keyword_dict.items() if keyword_counts[k] >= 1 or len(k.split()) == 1}

    # Sort the keywords by frequency and return the top 100 most common keywords with their count and associated URLs
    sorted_keywords = sorted(filtered_keywords.items(), key=lambda x: (-keyword_counts[x[0]], x[0]))
    return [(k, keyword_counts[k], v) for k, v in sorted_keywords[:100]]

if __name__ == '__main__':
    base_url = 'https://www.bogleheads.org'
    titles_with_urls = get_post_titles(base_url)
    keywords = get_keywords(titles_with_urls)

    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    # You can print or display the keywords if needed
    print(keywords)

