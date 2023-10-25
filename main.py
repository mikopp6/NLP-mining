import spacy
import itertools
from fuzzywuzzy import fuzz, process
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
from googlesearch import search
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import statistics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


import pandas as pd

def simple_search(query, num_results):
    results = search(query, num_results=num_results, advanced=True)
    return results

def clean_text(snippets):
    cleaned_snippets = []

    for snippet in snippets:
        tokenized = word_tokenize(snippet)
        word_array = []
        for word in tokenized:
            if word.isalpha():
                word_array.append(word)
        cleaned_string = ' '.join([str(word) for word in word_array])
        cleaned_snippets.append(cleaned_string)
        
    return cleaned_snippets



# Save
def save_to_file(snippets, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for snippet in list(snippets):
            file.write(snippet.description + "\n")

# Load
def load_from_file(filename):
    with open(filename, "r", encoding='utf-8') as file:
        snippets = file.read().splitlines()
    return snippets

# String matching
def string_matching(snippets):
    unique_index_pair_list = itertools.combinations(range(0,len(snippets)), 2)

    exact_matches = 0
    ratios = []
    for i, j in unique_index_pair_list:
        ratio = fuzz.ratio(snippets[i], snippets[j])
        if ratio == 100:
            exact_matches += 1
        ratios.append(ratio)
        
    return exact_matches, ratios

# Sentiment polarity
def sentiment_polarity(snippets):
    sentiment_polarities = []
    for snippet in snippets:
        polarity = TextBlob(snippet, analyzer=NaiveBayesAnalyzer()).polarity
        sentiment_polarities.append(polarity)
    return sentiment_polarities

# Wordcloud
def create_wordcloud(snippets):
    cloud = WordCloud(collocations=False, scale=4).generate(snippets).to_image()
    return cloud

# Named entity string matching
def named_entity_matching(snippets):
    nlp = spacy.load("en_core_web_sm")
    all_named_entities = []
    for snippet in snippets:
        named_entities = ""
        doc = nlp(snippet)
        for ent in doc.ents:
            named_entities += ent.text
        if named_entities != "":
            all_named_entities.append(named_entities.rstrip())

    return string_matching(all_named_entities)

def create_plots(tab, data, title1, title2, xlabel, ylabel):
    for plot_num in range(2):
        fig = Figure(figsize=(3, 2), dpi=100)
        ax = fig.add_subplot(111)
        if plot_num == 0:
            ax.set_title(title1)
        elif plot_num == 1:
            ax.set_title(title2)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        y = data[plot_num]
        x = [i for i in range(10, 101, 10)]
        ax.set_xticks(x)
        ax.plot(x, y, label="Data")
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

def create_combined_plot(tab, data, title, xlabel, ylabel):
    fig = Figure(figsize=(6, 4), dpi=100)  # Larger figure size
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    for plot_num in range(2):
        y = data[plot_num]
        x = [i for i in range(10, 101, 10)]
        ax.plot(x, y, label=f"Data {plot_num + 1}")

    ax.set_xticks(x)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

        
def generate_data(num_results, query):
    snippets = []
    
    if local_data_checkbox_var.get():
        if "site" in query:
            filename = "saved_search_data/snippets2.txt"
        else:
            filename = "saved_search_data/snippets1.txt"
        
        data = load_from_file(filename)
    else:
        print("Using search data")
        data = simple_search(query, num_results)

    for i, result in enumerate(data):
        if local_data_checkbox_var.get():
            snippets.append(result)
        else:
            snippets.append(result.description)
        if i >= num_results-1:
            break

    cleaned = clean_text(snippets)

    V1_all = []
    V2_all = []
    V3_all = []
    V4_all = []
    V5_all = []

    for i in range(10,110,10):
        V1 = 0
        V2 = 0
        V3 = 0
        V4 = 0
        V5 = 0

        if named_entity_checkbox_var.get():
            V1, ratios = named_entity_matching(cleaned[0:i])
        else:
            V1, ratios = string_matching(cleaned[0:i])
        V2 = statistics.mean(ratios)
        V3 = statistics.stdev(ratios)

        sentiment_polarities = sentiment_polarity(cleaned[0:i])
        V4 = statistics.mean(sentiment_polarities)
        V5 = statistics.stdev(sentiment_polarities)

        V1_all.append(V1)
        V2_all.append(V2)
        V3_all.append(V3)
        V4_all.append(V4)
        V5_all.append(V5)

    data = {"V1": V1_all, "V2": V2_all, "V3": V3_all, "V4": V4_all, "V5": V5_all}
    return data

def on_search_click():
    query1 = entry1.get()
    query2 = entry2.get()
    query2_formatted = f"{query1} site:{query2}"
    data1 = generate_data(100, query1)
    data2 = generate_data(100, query2_formatted)

    for i in range(1,6):
        data = [data1[f"V{i}"], data2[f"V{i}"]]
        tab = ttk.Frame(root)
        notebook.add(tab, text=f"V{i}")
        title = f"V{i} - {query1} vs {query2_formatted}"
        title1 = f"V{i} - '{query1}'"
        title2 = f"V{i} - '{query2_formatted}'"
        xlabel = "Number of snippets"
        if i == 1:
            ylabel = "Num of 100% matches"
        elif i == 2:
            ylabel = "Average string match ratio %"    
        elif i == 3:
            ylabel = "Standard deviation for string match ratio"    
        elif i == 4:
            ylabel = "Average sentiment polarity"  
        elif i == 5:
            ylabel = "Standard deviation for sentiment polarity"  
        
        if create_separate_plots_checkbox_var.get():
            create_plots(tab, data, title1, title2, xlabel, ylabel)
        else:    
            create_combined_plot(tab, data, title, xlabel, ylabel)
    
    

          

root = tk.Tk()
root.title("NLP Mining")
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

label1 = tk.Label(root, text="Search term")
label1.pack()
entry1 = tk.Entry(root)
entry1.insert(0, "carbon footprint") 
entry1.pack()
label2 = tk.Label(root, text="VS website")
label2.pack()
entry2 = tk.Entry(root)
entry2.insert(0, "www.bbc.com") 
entry2.pack()

named_entity_checkbox_var = tk.IntVar()
checkbox1 = tk.Checkbutton(root, text="Use named entities for string matching", variable=named_entity_checkbox_var)
checkbox1.pack()

local_data_checkbox_var = tk.IntVar()
checkbox2 = tk.Checkbutton(root, text="Use local data", variable=local_data_checkbox_var)
checkbox2.pack()

create_separate_plots_checkbox_var = tk.IntVar()
checkbox3 = tk.Checkbutton(root, text="Create separate plots", variable=create_separate_plots_checkbox_var)
checkbox3.pack()

search_button = tk.Button(root, text="Search", command=on_search_click)
search_button.pack()

root.mainloop()

