import sqlite3

def initialize_database():
    conn = sqlite3.connect('keywords.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY,
            keyword TEXT NOT NULL,
            count INTEGER NOT NULL,
            urls TEXT,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_keywords_to_database(keywords, year, month):
    conn = sqlite3.connect('keywords.db')
    c = conn.cursor()

    for keyword, count, url_list in keywords:
        url_string = ",".join(url_list)
        c.execute('''
            INSERT INTO keywords (keyword, count, urls, year, month)
            VALUES (?, ?, ?, ?, ?)
        ''', (keyword, count, url_string, year, month))

    conn.commit()
    conn.close()

def get_keywords_from_database(year, month):
    conn = sqlite3.connect('keywords.db')
    c = conn.cursor()

    c.execute('''
        SELECT keyword, count, urls
        FROM keywords
        WHERE year = ? AND month = ?
    ''', (year, month))

    keywords = c.fetchall()
    conn.close()

    # Convert the URLs strings back into lists
    keywords_with_urls = [(k, c, urls.split(',')) for k, c, urls in keywords]
    return keywords_with_urls
