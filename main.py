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
    with open(filename, "r") as file:
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
        all_named_entities.append(named_entities.rstrip())

    unique_index_pair_list = itertools.combinations(range(0,len(all_named_entities)), 2)

    exact_matches = 0
    ratios = []
    for i, j in unique_index_pair_list:
        ratio = fuzz.ratio(all_named_entities[i], all_named_entities[j])
        if ratio == 100:
            exact_matches += 1
        ratios.append(ratio)
        
    return exact_matches, ratios

def create_plots(tab, data, title):
    for plot_num in range(2):
        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(title)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        y = data[plot_num]
        x = [i for i in range(10, 101, 10)]
        ax.plot(x, y, label="Data")
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
def generate_data(num_results, query):
    data = simple_search(query, num_results)
    snippets = []
    for i, result in enumerate(data):
        snippets.append(result.description)
        if i >= num_results-1:
            break

    cleaned = clean_text(snippets)

    V1_all = []
    V2_all = []
    V3_all = []

    for i in range(10,110,10):
        V1 = 0
        V2 = 0
        V3 = 0

        V1, ratios = string_matching(cleaned[0:i])
        V2 = statistics.mean(ratios)
        V3 = statistics.stdev(ratios)

        V1_all.append(V1)
        V2_all.append(V2)
        V3_all.append(V3)
    
    data = {"V1": V1_all, "V2": V2_all, "V3": V3_all}
    return data

def on_button_click():
    query1 = entry1.get()
    query2 = entry2.get()
    data1 = generate_data(100, query1)
    data2 = generate_data(100, query2)

    for i in range(1,4):
        data = [data1[f"V{i}"], data2[f"V{i}"]]
        tab = ttk.Frame(root)
        notebook.add(tab, text=f"V{i}")
        create_plots(tab, data, title=f"Title {i}")

    
    

          

root = tk.Tk()
root.title("NLP Mining")
root.geometry("1000x600")
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

entry1 = tk.Entry(root)
entry1.pack()
entry2 = tk.Entry(root)
entry2.pack()

search_button = tk.Button(root, text="Search", command=on_button_click)
search_button.pack()

root.mainloop()

