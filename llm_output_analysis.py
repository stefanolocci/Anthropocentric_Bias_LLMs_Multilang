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