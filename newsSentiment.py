from textblob import TextBlob
import statistics
import matplotlib.pyplot as plt
import numpy as np

with open("bbc_cleaned_snippets.txt", "r") as file:
    snippets = file.read().splitlines()

V4_all = []
V5_all = []

for num_snippets in range(10, 110, 10):
    sentiment_polarities = []
    for snippet in snippets[0:num_snippets]:
        sentiment_polarity = TextBlob(snippet).sentiment[0]
        sentiment_polarities.append(sentiment_polarity)
    V4_all.append(statistics.mean(sentiment_polarities))
    V5_all.append(statistics.stdev(sentiment_polarities))

print(V4_all)
print(V5_all)

plt.plot(range(10,110,10), V4_all, 'bo')
plt.xticks(np.arange(10,110,10))
plt.ylabel("Average sentiment polarity")
plt.xlabel("Number of snippets")
plt.title("V4 - Query 'carbon footprint")
plt.show()

plt.plot(range(10,110,10), V5_all, 'ro')
plt.xticks(np.arange(10,110,10))
plt.ylabel("Standard deviation of average sentiment polarity")
plt.xlabel("Number of snippets")
plt.title("V5 - Query 'carbon footprint'")
plt.show()