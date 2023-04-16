import datetime
from database import save_keywords_to_database, initialize_database

# Adjusted mock data for the prior month
mock_keywords = [
    # ...(existing unigram data)
    ("mutual fund", 200, ["https://example.com/post11", "https://example.com/post12"]),
    ("index fund", 150, ["https://example.com/post13", "https://example.com/post14"]),
    ("ETF", 125, ["https://example.com/post15", "https://example.com/post16"]),
    ("dividend", 100, ["https://example.com/post17", "https://example.com/post18"]),
    ("tax", 90, ["https://example.com/post19", "https://example.com/post20"]),
    ("roth", 9, ["https://example.com/post21", "https://example.com/post22"]),
    ("box", 2, []),
    # Add bigrams
    ("investment portfolio", 80, ["https://example.com/post23", "https://example.com/post24"]),
    ("stock market", 70, ["https://example.com/post25", "https://example.com/post26"]),
    ("bond market", 60, ["https://example.com/post27", "https://example.com/post28"]),
    ("retirement plan", 50, ["https://example.com/post29", "https://example.com/post30"]),
    ("money market", 2, []),
    # Add trigrams
    ("low-cost index fund", 40, ["https://example.com/post31", "https://example.com/post32"]),
    ("tax-efficient investing", 30, ["https://example.com/post33", "https://example.com/post34"]),
    ("money market funds", 4, ["https://example.com/post33", "https://example.com/post34", "https://example.com/post331"]),
    ("long-term investment strategy", 20, ["https://example.com/post35", "https://example.com/post36"]),
]

def generate_mock_data(base_data):
    new_data = []
    for k, v, u in base_data:
        new_count = max(v, 0)
        new_urls = u[:new_count]
        new_data.append((k, new_count, new_urls))
    return new_data

def mock():
    initialize_database()

    # Get the previous month and year
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    previous_month, previous_year = current_month - 1, current_year
    if previous_month == 0:
        previous_month, previous_year = 12, previous_year - 1

    # Generate and save the mock data for the prior month
    prior_month_data = generate_mock_data(mock_keywords)
    save_keywords_to_database(prior_month_data, previous_year, previous_month)

if __name__ == "__main__":
    mock()