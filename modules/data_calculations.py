""" Data calculations """
from collections import Counter
from itertools import islice


def count_words(titles: list) -> dict:
  """
  Count word occurrences.

  :param titles: List of article titles.

  :return: Word occurrences.
  """
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


def join_words_amount(
  final_counts: dict, calculated_amounts: dict
) -> dict:
  """
  Joins calculated words amount into final dictionary.

  :param final_counts: Dictionary that stores all results.
  :param calculated_amounts: Dictionary that stores results from actual scraper.

  :return: Dictionary with merged words count.
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

  :return: Dictionary with sorted words amount. Top 10 words count.
  """
  for k in final_counts:
    final_counts[k] = dict(
      sorted(final_counts[k].items(), key=lambda item: item[1], reverse=True)
    )
  return {
    key: dict(islice(value.items(), 10))
    for key, value in final_counts.items()
  }
