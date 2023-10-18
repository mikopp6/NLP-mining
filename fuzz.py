from fuzzywuzzy import fuzz, process
from itertools import combinations
import statistics
import matplotlib.pyplot as plt
import numpy as np

with open("bbc_cleaned_snippets.txt", "r") as file:
    snippets = file.read().splitlines()

V1_all = []
V2_all = []
V3_all = []
ratios_all = []


for num_snippets in range(10, 110, 10):
    similar_count = 0
    ratios = []
    for snippet in snippets[0:num_snippets]:
        ratio = fuzz.partial_ratio("carbon footprint", snippet)
        if ratio == 100:
            similar_count += 1
        ratios.append(ratio)
    V1_all.append(similar_count)
    V2_all.append(statistics.mean(ratios))
    V3_all.append(statistics.stdev(ratios))

print(V1_all)
print(V2_all)
print(V3_all)

plt.plot(range(10,110,10), V1_all, 'bo')
plt.xticks(np.arange(10,110,10))
plt.ylabel("Number of 100% matches")
plt.xlabel("Number of snippets")
plt.title("V1 - Query 'carbon footprint")
plt.show()

plt.plot(range(10,110,10), V2_all, 'ro')
plt.xticks(np.arange(10,110,10))
plt.ylabel("Average string match ratio %")
plt.xlabel("Number of snippets")
plt.title("V2 - Query 'carbon footprint'")
plt.show()

plt.plot(range(10,110,10), V3_all)
plt.xticks(np.arange(10,110,10))
plt.ylabel("Standard deviation of average value")
plt.xlabel("Number of snippets")
plt.title("V3 - Query 'carbon footprint'")
plt.show()
