""" Pages operations """
import json

import requests
from bs4 import BeautifulSoup

from modules.data_calculations import count_words, join_words_amount


def read_input_json(name: str) -> list:
  """
  Reads input data from JSON file.

  :param name: Input file name.

  :return: List of pages data.
  """
  try:
    with open(name, "r") as f:
      input_data = json.load(f)
      return input_data["pages"]
  except FileNotFoundError:
    print("File does not exist!")
    return []


def get_page_titles(page_url: str, html_tag: str, html_class: str) -> list:
  """
  Scrapes articles titles from given page.

  :param page_url: Page url.
  :param html_tag: HTML tag to scrape.
  :param html_class: HTML class to scrape.

  :return: List of articles titles.
  """
  try:
    page = requests.get(page_url)
  except requests.exceptions.Timeout:
    print("Timeout occurred!")
    return []
  soup = BeautifulSoup(page.content, "html.parser")
  elements = soup.find_all(html_tag, {"class": html_class})
  return [
    element.text.replace("\xa0", " ").replace("\n", "").strip()
    for element in elements]


def process_pages(pages_data: dict) -> [dict, int]:
  """
  Extracts articles titles and counts word amount in category.

  :param pages_data: Dictionary with pages data.

  :return: Dictionary with calculates words and amount of titles.
  """
  words_data = {}
  titles_amount = 0
  for page_data in pages_data:
    url = page_data["url"]
    categories = page_data["categories"]
    print("First three titles for every URL.")
    print(f"====== {url} - {categories} ======")
    html_tag = page_data["tag"]
    html_class = page_data["class"]
    titles = get_page_titles(url, html_tag, html_class)
    print(f"Found {len(titles)} titles.")
    print(titles[:3])
    titles_amount += len(titles)
    words_amount = count_words(titles)
    print("============")
    words_amount_with_categories = {
        category: words_amount
        for category in categories
    }
    words_data = join_words_amount(words_data, words_amount_with_categories)
  return words_data, titles_amount


def split_pages_data(input_data: list) -> [list, list, list, list]:
  """
  Splits given pages data into 4 smaller lists.

  :param input_data: List of pages data.

  :return: 4 smaller slices of pages data.
  """
  splitter = len(input_data) // 4
  part1 = input_data[:splitter]
  part2 = input_data[splitter:2 * splitter]
  part3 = input_data[2 * splitter:3 * splitter]
  part4 = input_data[3 * splitter:]
  return [part1, part2, part3, part4]
