import spacy
import os
import json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

# Load spaCy's English tokenizer
nlp = spacy.load("en_core_web_sm")

def get_text(directory):
    # Initializes strings to hold concatenated prompts
    texts = {"neutral": "", "anthropocentric": "", "ecocentric": ""}
    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                texts["neutral"] += data.get("neutral_prompt", "") + " "
                texts["anthropocentric"] += data.get("anthropocentric_prompt", "") + " "
                texts["ecocentric"] += data.get("ecocentric_prompt", "") + " "
    return texts

def process_text(text):
    # Tokenize, remove stopwords, and generate unigrams
    doc = nlp(text)
    unigrams = [token.lemma_.lower().strip() for token in doc if not token.is_stop and not token.is_punct]

    # Generate bigrams
    bgrms = [' '.join(bigram) for bigram in bigrams(unigrams)]

    # Combine unigrams and bigrams
    combined = unigrams
    return ' '.join(combined)

def generate_wordcloud(text, title):
    # Create stopword list:
    stopwords = set(STOPWORDS)
    stopwords.update(["anthropocentric", "viewpoint", "crucial", "role"])
    # Generate the word cloud
    wordcloud = WordCloud(stopwords=stopwords, width = 800, height = 400, max_words=200, background_color ='white').generate(text)
    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis("off")
    plt.show()

directory = '/content/drive/MyDrive/Anthropocentric_Bias/gpt/output/'
texts = get_text(directory)

for key, text in texts.items():
    processed_text = process_text(text)
    generate_wordcloud(processed_text, f"Word Cloud for {key.capitalize()} Prompts")