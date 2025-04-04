# Pages articles web scraper

### Version: 2.0.0

## About 📈

An application that scrapes pages articles titles based on given input JSON data.

Main features:
- extracting articles titles in threads
- division of pages into categories
- calculating words amount in titles
- displaying category results on bar charts

## Technology 💻
The application was written in Python 3.11.

Libraries used
- beautifulsoup4
- requests
- matplotlib
- concurrent.futures
- collections
- itertools
- json

## How to use ⚙
Do following steps:
1. Clone the repository: `git clone https://github.com/g-boron/PagesArticlesScraper.git`
2. Install required libraries: `pip install -r requirements.txt`
3. Prepare data or use predefined in `input/input.json`
4. Run the application: `python main.py`

## License 📑

Open source [MIT](https://opensource.org/license/mit) license.