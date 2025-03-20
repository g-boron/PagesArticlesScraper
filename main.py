""" Main module """
import json
from collections import Counter

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

  :returns: Dictionary with sorted words amount.
  """
  for k in final_counts:
    final_counts[k] = dict(
      sorted(final_counts[k].items(), key=lambda item: item[1], reverse=True)
    )
  return final_counts


if __name__ == "__main__":
  data = read_input_json("input.json")
  words_count = {}
  for page_data in data:
    url = page_data["url"]
    categories = page_data["categories"]
    print(f"====== {url} - {categories} ======")
    html_tag = page_data["tag"]
    html_class = page_data["class"]
    titles = get_page_titles(url, html_tag, html_class)
    print(titles[:3])
    words_amount = count_words(titles)
    print(words_amount)
    print("============")
    words_amount_with_categories = {
        category: words_amount
        for category in categories
    }
    words_count = join_words_amount(words_count, words_amount_with_categories)

  words_counts = sort_dictionary(words_count)
  for category, words in words_count.items():
    words_list = []
    amounts = []
    for word, amount in words.items():
      if amount > 2:
        print(f"{word} - {amount}")
        words_list.append(word)
        amounts.append(amount)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(words_list, amounts)
    ax.bar_label(bars)
    plt.title(f"Category: {category}")
    plt.ylabel("Words amount")
    plt.xlabel("Word")
    plt.show()
