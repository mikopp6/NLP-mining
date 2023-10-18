from wordcloud import WordCloud

text = open("bbc_cleaned_snippets.txt").read()

WordCloud(collocations=False, scale=4).generate(text).to_file("wordcloud.png")