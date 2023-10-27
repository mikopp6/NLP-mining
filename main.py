import spacy
import itertools
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS
from googlesearch import search
import tkinter as tk
from tkinter import ttk
import statistics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer




REMOVE_LIST = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

#
# Utility functions
#

# Clean text, tokenize into words
def clean_text(snippets):
    cleaned_snippets = []

    for snippet in snippets:
        tokenized = word_tokenize(snippet)
        word_array = []
        for word in tokenized:
            if word.isalpha() and word.lower() not in REMOVE_LIST:
                word_array.append(word)
        cleaned_string = ' '.join([str(word) for word in word_array])
        cleaned_snippets.append(cleaned_string)
        
    return cleaned_snippets

# Save snippets to file
def save_to_file(snippets, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for snippet in list(snippets):
            file.write(snippet.description + "\n")

# Load snippets from file
def load_from_file(filename):
    with open(filename, "r", encoding='utf-8') as file:
        snippets = file.read().splitlines()
    return snippets


def on_search_click():
    query1 = entry1.get()
    query2 = entry2.get()
    query2_formatted = f"{query1} site:{query2}"
    start_analysis(query1, query2_formatted)


#
# Task functions
#

# Task 1, Snippet retrieval
def simple_search(query, num_results):
    results = search(query, num_results=num_results, advanced=True)
    return results

# Task 2 & 6, String matching with FuzzyWuzzy
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

# Task 3 & 6, Sentiment polarity analysis with TextBlob NaiveBayesAnalyzer
def sentiment_polarity(snippets, textblobber):
    sentiment_polarities = []
    for snippet in snippets:
        polarity = textblobber(snippet).polarity
        sentiment_polarities.append(polarity)
    return sentiment_polarities

# Task 4 & 6, Named entity string matching
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

# Task 5 & 7, Wordcloud
def create_wordcloud(snippets, extra_stopwords):
    text = " ".join(snippets)
    stopwords = extra_stopwords + list(STOPWORDS)
    wordcloud = WordCloud(stopwords=stopwords, width=800, height=600).generate(text)
    return wordcloud

#
# Plotting functions
#


# Creates combined line plot, packs it into tab
def create_combined_plot(tab, data, title, xlabel, ylabel):
    fig = Figure(figsize=(6, 4), dpi=100)
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

# Creates box plots, packs them into tab
def create_boxplots(tab, data, title1, title2):
    for plot_num in range(2):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.boxplot(data[plot_num])
        if plot_num == 0:
            ax.set_title(title1)
        elif plot_num == 1:
            ax.set_title(title2)
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

# Creates error plot, packs them into tab
def create_errorbars(tab, means, errors, yticks, title1, title2, ylabel):
    for plot_num in range(2):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        y = means[plot_num]
        x = [i for i in range(10, 101, 10)]
        error = errors[plot_num]
        ax.errorbar(x, y, error, ecolor="red")
        if plot_num == 0:
            ax.set_title(title1)
        elif plot_num == 1:
            ax.set_title(title2)
        ax.set_xticks(x)
        ax.set_yticks(yticks)
        ax.set_xlabel("Number of snippets")
        ax.set_ylabel(ylabel)
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

# Plots wordclouds, packs them into tab
def plot_wordclouds(tab, data, title1, title2):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    for plot_num in range(2):
        axes[plot_num].imshow(data[plot_num], interpolation='bilinear')
        if plot_num == 0:
            axes[plot_num].set_title(title1)
        elif plot_num == 1:
            axes[plot_num].set_title(title2)
        axes[plot_num].axis("off")

    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
        

#
# Program functions
#

# Generates data to be shown in GUI 
def generate_data(num_results, query, textblobber):
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

    string_match_ratios_all = []
    sentiment_polarities_all = []
    V1_all = []
    V2_all = []
    V3_all = []
    V4_all = []
    V5_all = []
    extra_stopwords = query.split()
    wordcloud = create_wordcloud(cleaned, extra_stopwords)

    for i in range(10,110,10):
        V1 = 0
        V2 = 0
        V3 = 0
        V4 = 0
        V5 = 0
        ratios = []

        if named_entity_checkbox_var.get():
            V1, ratios = named_entity_matching(cleaned[0:i])
        else:
            V1, ratios = string_matching(cleaned[0:i])
        V2 = statistics.mean(ratios)
        V3 = statistics.stdev(ratios)

        sentiment_polarities = sentiment_polarity(cleaned[0:i], textblobber)
        V4 = statistics.mean(sentiment_polarities)
        V5 = statistics.stdev(sentiment_polarities)

        string_match_ratios_all.append(ratios)
        sentiment_polarities_all.append(sentiment_polarities)
        V1_all.append(V1)
        V2_all.append(V2)
        V3_all.append(V3)
        V4_all.append(V4)
        V5_all.append(V5)

    data = {"sm": string_match_ratios_all, "sp": sentiment_polarities_all, "V1": V1_all, "V2": V2_all, "V3": V3_all, "V4": V4_all, "V5": V5_all, "V6": wordcloud}
    return data

# The main part of the program, retrieves data and plots according to user choice
def start_analysis(query1, query2):
    # Create textblobber here to increase performance
    textblobber = Blobber(analyzer=NaiveBayesAnalyzer())

    data1 = generate_data(100, query1, textblobber)
    data2 = generate_data(100, query2, textblobber)

    print("data generated")

    if selected_plot_type_var.get() == "error":
        tab = ttk.Frame(root)
        notebook.add(tab, text="String matching")
        means = [data1[f"V{2}"], data2[f"V{2}"]]
        errors = [data1[f"V{3}"], data2[f"V{3}"]]
        title1 = f"String match percentage - '{query1}'"
        title2 = f"String match percentage - '{query2}'"
        ylabel = "Average string match score"
        create_errorbars(tab, means, errors, range(0,110,10), title1, title2, ylabel)

        tab = ttk.Frame(root)
        notebook.add(tab, text="Sentiment polarities")
        means = [data1[f"V{4}"], data2[f"V{4}"]]
        errors = [data1[f"V{5}"], data2[f"V{5}"]]
        title1 = f"Sentiment polarity - '{query1}'"
        title2 = f"Sentiment polarity - '{query2}'"
        ylabel = "Average sentiment polarity"
        create_errorbars(tab, means, errors, [(x/10) for x in range(-10, 11, 1)], title1, title2, ylabel)

        tab = ttk.Frame(root)
        notebook.add(tab, text="Wordclouds")
        data = [data1["V6"], data2["V6"]]
        title1 = f"'{query1}'"
        title2 = f"'{query2}'"
        plot_wordclouds(tab, data, title1, title2)
    elif selected_plot_type_var.get()=="line":
        for i in range(1,7):
            tab = ttk.Frame(root)
            notebook.add(tab, text=f"V{i}")
            data = [data1[f"V{i}"], data2[f"V{i}"]]
            title = f"V{i} - {query1} vs {query2}"
            title1 = f"V{i} - '{query1}'"
            title2 = f"V{i} - '{query2}'"
            if i == 6:
                plot_wordclouds(tab, data, title1, title2)
                break
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

            create_combined_plot(tab, data, title, xlabel, ylabel)
    elif selected_plot_type_var.get() == "box":
        tab = ttk.Frame(root)
        notebook.add(tab, text="String matching")
        data = [data1["sm"], data2["sm"]]
        title1 = f"String match percentage - '{query1}'"
        title2 = f"String match percentage - '{query2}'"
        create_boxplots(tab, data, title1, title2)

        tab = ttk.Frame(root)
        notebook.add(tab, text="Sentiment polarities")
        data = [data1["sp"], data2["sp"]]
        title1 = f"Sentiment polarity - '{query1}'"
        title2 = f"Sentiment polarity - '{query2}'"
        create_boxplots(tab, data, title1, title2)

        tab = ttk.Frame(root)
        notebook.add(tab, text="Wordclouds")
        data = [data1["V6"], data2["V6"]]
        title1 = f"'{query1}'"
        title2 = f"'{query2}'"
        plot_wordclouds(tab, data, title1, title2)



# GUI code
root = tk.Tk()
root.title("NLP Mining")
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)


tk.Label(frame, text="Search term").pack()
entry1 = tk.Entry(frame)
entry1.insert(0, "carbon footprint") 
entry1.pack()
tk.Label(frame, text="VS website").pack()
entry2 = tk.Entry(frame)
entry2.insert(0, "www.bbc.com") 
entry2.pack()

named_entity_checkbox_var = tk.IntVar()
tk.Checkbutton(frame, text="Named entities", variable=named_entity_checkbox_var).pack()

local_data_checkbox_var = tk.IntVar()
tk.Checkbutton(frame, text="Local data", variable=local_data_checkbox_var).pack()

selected_plot_type_var = tk.StringVar(value="error")
tk.Radiobutton(frame, text="Error plot", variable=selected_plot_type_var, value="error").pack(side="left")
tk.Radiobutton(frame, text="Box plot", variable=selected_plot_type_var, value="box").pack(side="left")
tk.Radiobutton(frame, text="Line plot", variable=selected_plot_type_var, value="line").pack(side="left")

tk.Button(root, text="Search", command=on_search_click).pack(side="bottom")

root.mainloop()

