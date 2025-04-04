""" Displaying data """
import matplotlib.pyplot as plt


def display_charts(final_counts: dict) -> None:
  """
  Generates bar charts with words amount aggregation.

  :param final_counts: Dictionary of result data.
  """
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
