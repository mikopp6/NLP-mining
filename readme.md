
1. I used https://pypi.org/project/googlesearch-python/ to scrape 100 results from google search “carbon footprint”. 
    - Code for this in ```simple_search.py```. I cleaned the result snippets manually, removing beginning dates and trailing dots


2. I used FuzzyWuzzy partial ratio string matching on an increasing groups of search result snippets (10, 20, 30...100) to figure out three values. 
	- Code for this in ```fuzz.py```
    - Number of 100% ratio matches
		![](/img/fig2_1.png)
    - Average ratios
		![](/img/fig2_2.png)
    - Standard deviation of ratios. 
		![](/img/fig2_3.png)

	- The graphs show that there are a lot of 100% matches at the beginning, but they lessen as more snippets are included. The average ratio also decreases steadily from 99% to 84%, with the standard deviation increasing from 3% to 21%.


3. 
	- Code for this in ```sentiment.py```

4. 

5. 
	- Code for this in ```wordcloud_gen.py```
	![](/img/wordcloud.png)

6. 

7. 

8. 

9. 