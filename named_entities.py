import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("ICAO Carbon Emissions Calculator (ICEC). Resume. ​. ICAO has developed a methodology to calculate the carbon dioxide emissions from air travel for use in.")

for ent in doc.ents:
    print(ent.text)