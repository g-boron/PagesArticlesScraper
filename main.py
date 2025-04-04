""" Main module """
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor

from modules.pages_operations import (
  read_input_json, process_pages, split_pages_data
)
from modules.data_calculations import sort_dictionary, join_words_amount
from modules.visualisations import display_charts


if __name__ == "__main__":
  data = read_input_json("input/input.json")
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
