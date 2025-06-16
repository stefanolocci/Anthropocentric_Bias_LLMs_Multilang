import spacy
import nltk
from nltk.util import bigrams
from collections import Counter

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def calculate_word_overlap(doc1, doc2, name1, name2):
    # Preprocessing: remove newline characters
    doc1 = doc1.replace('\n', ' ')
    doc2 = doc2.replace('\n', ' ')

    # Step 1: Tokenize, lemmatize, and remove stopwords and punctuation
    tokens1 = [token.lemma_.lower() for token in nlp(doc1) if not token.is_stop and not token.is_punct]
    tokens2 = [token.lemma_.lower() for token in nlp(doc2) if not token.is_stop and not token.is_punct]

    # Step 2: Create sets of lemmatized words
    set1 = set(tokens1)
    set2 = set(tokens2)

    # Step 3: Find intersection of both sets
    intersection = set1.intersection(set2)
    # Step 4: Count occurrences in both documents
    count1 = Counter(tokens1)
    count2 = Counter(tokens2)

    # Collecting the intersection and counts
    result = {}
    for word in intersection:
        result[word] = {f'count_in_{name1}': count1[word], f'count_in_{name2}': count2[word]}

    return result



def calculate_bigram_overlap(doc1, doc2, name1, name2):
    # Preprocessing: remove newline characters
    doc1 = doc1.replace('\n', ' ')
    doc2 = doc2.replace('\n', ' ')

    # Step 1: Tokenize, lemmatize, and remove stopwords and punctuation
    tokens1 = [token.lemma_.lower() for token in nlp(doc1) if not token.is_stop and not token.is_punct]
    tokens2 = [token.lemma_.lower() for token in nlp(doc2) if not token.is_stop and not token.is_punct]

    # Step 2: Generate bigrams using NLTK
    bigrams1 = [' '.join(bigram) for bigram in bigrams(tokens1)]
    bigrams2 = [' '.join(bigram) for bigram in bigrams(tokens2)]

    # Convert bigrams to sets
    set1 = set(bigrams1)
    set2 = set(bigrams2)

    # Step 3: Find intersection of both sets of bigrams
    intersection = set1.intersection(set2)

    # Step 4: Count occurrences of each bigram in both documents
    count1 = Counter(bigrams1)
    count2 = Counter(bigrams2)

    # Collecting the intersection and counts
    result = {}
    for bigram in intersection:
        result[bigram] = {f'count_in_{name1}': count1[bigram], f'count_in_{name2}': count2[bigram]}

    return result

"""## Save unigrams and bigrams overlap"""

import json

# Load the JSON file
with open(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/output/{experiment_name}.json', 'r') as file:
    data = json.load(file)

# Use the specific fields from the JSON data
res_1 = calculate_word_overlap(data["neutral_prompt"], data["anthropocentric_prompt"], "neutral", "anthropocentric")
res_2 = calculate_word_overlap(data["neutral_prompt"], data["ecocentric_prompt"], "neutral", "ecocentric")

res_b_1 = calculate_bigram_overlap(data["neutral_prompt"], data["anthropocentric_prompt"], "neutral", "anthropocentric")
res_b_2 = calculate_bigram_overlap(data["neutral_prompt"], data["ecocentric_prompt"], "neutral", "ecocentric")

# Save the result to a JSON file
with open(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/words_stats/unigrams/{experiment_name}_neutral_anth.json',
          'w') as file:
    json.dump(res_1, file, indent=4)

with open(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/words_stats/unigrams/{experiment_name}_neutral_eco.json',
          'w') as file:
    json.dump(res_2, file, indent=4)

# Save the result to a JSON file
with open(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/words_stats/bigrams/{experiment_name}_neutral_anth.json',
          'w') as file:
    json.dump(res_b_1, file, indent=4)

with open(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/words_stats/bigrams/{experiment_name}_neutral_eco.json',
          'w') as file:
    json.dump(res_b_2, file, indent=4)
