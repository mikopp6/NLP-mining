from googlesearch import search
from pprint import pprint

results = search("carbon footprint site:www.bbc.com/news", num_results=100, advanced=True)

with open("snippets.txt", "w", encoding="utf-8") as file:
    for result in list(results):
        file.write(result.description + "\n")
    