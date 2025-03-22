""" Main module """
import json
from collections import Counter
from itertools import islice
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def read_input_json(name):
  with open(name, "r") as f:
    input_data = json.load(f)
    return input_data["pages"]


def get_page_titles(page_url, html_tag, html_class):
  page = requests.get(page_url)
  soup = BeautifulSoup(page.content, "html.parser")
  elements = soup.find_all(html_tag, {"class": html_class})
  return [
    element.text.replace("\xa0", " ").replace("\n", "").strip()
    for element in elements]


def count_words(titles):
  result = {}
  for title in titles:
    title = title.split(" ")
    title = [word.lower() for word in title]
    counter = dict(Counter(title))
    for word, amount in counter.items():
      if word in result:
        result[word] += amount
      else:
        result[word] = amount
  return result


def join_words_amount(final_counts, calculated_amounts) -> dict:
  """
  Joins calculated words amount into final dictionary.

  :param final_counts: Dictionary that stores all results.
  :param calculated_amounts: Dictionary that stores results from actual scraper.

  :returns: Dictionary with merged words count.
  """
  for key, value in calculated_amounts.items():
    if key in final_counts:
      for sub_key, sub_value in value.items():
        if sub_key in final_counts[key]:
          final_counts[key][sub_key] += sub_value
        else:
          final_counts[key][sub_key] = sub_value
    else:
      final_counts[key] = value
  return final_counts


def sort_dictionary(final_counts: dict) -> dict:
  """
  Sorts dictionary by words amount.

  :param final_counts: Dictionary that stores all results.

  :returns: Dictionary with sorted words amount. Top 10 words count.
  """
  for k in final_counts:
    final_counts[k] = dict(
      sorted(final_counts[k].items(), key=lambda item: item[1], reverse=True)
    )
  return {
    key: dict(islice(value.items(), 10))
    for key, value in final_counts.items()
  }


def display_charts(final_counts):
  for category, words in final_counts.items():
    words_list = []
    amounts = []
    for word, amount in words.items():
      words_list.append(word)
      amounts.append(amount)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(words_list, amounts)
    ax.bar_label(bars)
    plt.title(
      f"Amount of words in category {category} with more than 2 occurrences.",
      fontsize=20
    )
    plt.ylabel("Words amount", fontsize=15)
    plt.xlabel("Word", fontsize=15)
    plt.show()


def process_pages(pages_data):
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


def split_pages_data(input_data):
  splitter = len(input_data) // 4
  part1 = data[:splitter]
  part2 = data[splitter:2 * splitter]
  part3 = data[2 * splitter:3 * splitter]
  part4 = data[3 * splitter:]
  return [part1, part2, part3, part4]


if __name__ == "__main__":
  data = read_input_json("input.json")
  print(f"Pages to scrape: {len(data)}")
  prepared_data = split_pages_data(data)
  start = perf_counter()
  with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
      executor.submit(process_pages, prepared_data[0]),
      executor.submit(process_pages, prepared_data[1]),
      executor.submit(process_pages, prepared_data[2]),
      executor.submit(process_pages, prepared_data[3])
    ]
    words_count = {}
    titles_count = 0
    for future in futures:
      words_count_future, titles_count_future = future.result()
      words_count = join_words_amount(words_count, words_count_future)
      titles_count += titles_count_future
  print(f"Pages processing took {round(perf_counter() - start, 2)} seconds.")
  print(f"Found total {titles_count} titles.")
  words_counts = sort_dictionary(words_count)
  display_charts(words_counts)
