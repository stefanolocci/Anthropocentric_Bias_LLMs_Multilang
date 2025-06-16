def write_list_to_json(my_list, filename):
    # Mapping list elements to specified labels
    data = {
        "neutral_prompt": my_list[0],
        "anthropocentric_prompt": my_list[1],
        "ecocentric_prompt": my_list[2]
    }

    # Writing JSON data to a file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def list_filenames(directory):
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return []

        # List all files in the given directory
        filenames = os.listdir(directory)

        # Remove the .json extension from filenames
        file_list = [os.path.splitext(file)[0] for file in filenames if file.endswith('.json')]

        # Print the list of filenames as a Python list
        print("filenames:", file_list)

        return file_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# Specify the directory to iterate through
directory_path = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/output"

# Get and print the list of filenames
list_filenames(directory_path)

filenames = ['what_are_animals_for', 'what_is_the_soil_for', 'what_is_the_soil_good_for', 'what_are_animals_good_for',
             'what_are_mountains_good_for', 'what_are_the_negative_effects_of_climate_change',
             'what_are_the_negative_effects_of_climate_change_on_humans',
             'what_are_the_negative_effects_of_climate_change_on_non_human_entities', 'pigs_are',
             'provide_a_description_of_chickens', 'provide_a_description_of_cows', 'provide_a_description_of_wolves',
             'provide_a_description_of_fishes', 'provide_a_description_of_trees', 'provide_a_description_of_soil',
             'provide_a_description_of_mountains', 'dogs_are', 'horses_are', 'sea_is', 'rivers_are']

"""# Aggregate outputs"""

import os
import json


def aggregate_prompts(input_directory, output_directory):
    try:
        # Check if the input directory exists
        if not os.path.exists(input_directory):
            print(f"Input directory not found: {input_directory}")
            return

        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Initialize lists to hold the aggregated prompts
        neutral_prompts = []
        anthropocentric_prompts = []
        ecocentric_prompts = []

        # Iterate through all .json files in the input directory
        for filename in os.listdir(input_directory):
            if filename.endswith('.json'):
                filepath = os.path.join(input_directory, filename)

                # Read the JSON file
                with open(filepath, 'r') as file:
                    data = json.load(file)

                # Append the prompts to their respective lists
                if "neutral_prompt" in data:
                    neutral_prompts.append(str(data["neutral_prompt"]))
                if "anthropocentric_prompt" in data:
                    anthropocentric_prompts.append(str(data["anthropocentric_prompt"]))
                if "ecocentric_prompt" in data:
                    ecocentric_prompts.append(str(data["ecocentric_prompt"]))

        # Save aggregated prompts to their respective files
        with open(os.path.join(output_directory, 'neutral_outputs.txt'), 'w') as file:
            file.write("\n".join(neutral_prompts))

        with open(os.path.join(output_directory, 'anthropocentric_outputs.txt'), 'w') as file:
            file.write("\n".join(anthropocentric_prompts))

        with open(os.path.join(output_directory, 'ecocentric_outputs.txt'), 'w') as file:
            file.write("\n".join(ecocentric_prompts))

        print(f"Aggregated outputs saved to {output_directory}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Specify input and output directories
input_directory = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/output"
output_directory = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs"

# Run the aggregation
aggregate_prompts(input_directory, output_directory)

"""# Extract noun_phrases

## Aggregated
"""

import os
import spacy
from google.colab import drive

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_noun_phrases_from_file(file_path):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Process the content with spaCy
        doc = nlp(content)

        # Extract noun phrases and convert to lowercase
        noun_phrases = {chunk.text.lower() for chunk in doc.noun_chunks if
                        not any(token.is_stop or token.is_punct for token in chunk)}

        return noun_phrases

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return set()


def extract_all_noun_phrases(input_files):
    try:
        # Extract noun phrases from each file and store in variables
        neutral_noun_phrases = extract_noun_phrases_from_file(input_files["neutral"])
        anthropocentric_noun_phrases = extract_noun_phrases_from_file(input_files["anthropocentric"])
        ecocentric_noun_phrases = extract_noun_phrases_from_file(input_files["ecocentric"])

        return neutral_noun_phrases, anthropocentric_noun_phrases, ecocentric_noun_phrases

    except Exception as e:
        print(f"An error occurred: {e}")
        return set(), set(), set()


# Specify the aggregated input files
input_files = {
    "neutral": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/neutral_outputs.txt",
    "anthropocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/anthropocentric_outputs.txt",
    "ecocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/ecocentric_outputs.txt",
}

# Run the extraction
neutral_noun_phrases, anthropocentric_noun_phrases, ecocentric_noun_phrases = extract_all_noun_phrases(input_files)


"""# Extract verbs

## Aggregated
"""

import os
import spacy
from google.colab import drive

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_verbs_from_file(file_path):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Process the content with spaCy
        doc = nlp(content)

        # Extract verbs and convert to lowercase
        verbs = {token.text.lower() for token in doc if token.pos_ == "VERB" and not (token.is_stop or token.is_punct)}

        return verbs

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        return set()


def extract_all_verbs(input_files):
    try:
        # Extract verbs from each file and store in variables
        neutral_verbs = extract_verbs_from_file(input_files["neutral"])
        anthropocentric_verbs = extract_verbs_from_file(input_files["anthropocentric"])
        ecocentric_verbs = extract_verbs_from_file(input_files["ecocentric"])

        return neutral_verbs, anthropocentric_verbs, ecocentric_verbs

    except Exception as e:
        print(f"An error occurred: {e}")
        return set(), set(), set()


# Specify the aggregated input files
input_files = {
    "neutral": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/neutral_outputs.txt",
    "anthropocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/anthropocentric_outputs.txt",
    "ecocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/ecocentric_outputs.txt",
}

# Run the extraction
neutral_verbs, anthropocentric_verbs, ecocentric_verbs = extract_all_verbs(input_files)


"""# Rankings

## Aggregated
"""

import os
import json
from collections import Counter


def count_occurrences(phrases, aggregated_files, output_file, phrase_type):
    try:
        # Initialize the result dictionary
        results = []

        # Read content from each aggregated file
        file_contents = {}
        for key, file_path in aggregated_files.items():
            with open(file_path, 'r') as file:
                file_contents[key] = file.read()

        # Count occurrences for each phrase (noun phrase or verb)
        for phrase in phrases:
            result = {
                phrase_type: phrase,
                "neutral_count": file_contents["neutral"].count(phrase),
                "anthropocentric_count": file_contents["anthropocentric"].count(phrase),
                "ecocentric_count": file_contents["ecocentric"].count(phrase),
            }
            results.append(result)

        # Write the results to the output JSON file
        with open(output_file, 'w') as file:
            json.dump(results, file, indent=4)

        print(f"{phrase_type.capitalize()} counts saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Aggregated input files
aggregated_files = {
    "neutral": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/neutral_outputs.txt",
    "anthropocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/anthropocentric_outputs.txt",
    "ecocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/ecocentric_outputs.txt",
}

# Specify output directories
output_dir_np = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/nouns_count"
output_dir_v = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/verbs_count"


# Process all categories for nouns and verbs
def process_all():
    # Noun phrases
    count_occurrences(
        neutral_noun_phrases,
        aggregated_files,
        os.path.join(output_dir_np, "neutral_noun_phrase_counts.json"),
        phrase_type="noun_phrase"
    )
    count_occurrences(
        anthropocentric_noun_phrases,
        aggregated_files,
        os.path.join(output_dir_np, "anthropocentric_noun_phrase_counts.json"),
        phrase_type="noun_phrase"
    )
    count_occurrences(
        ecocentric_noun_phrases,
        aggregated_files,
        os.path.join(output_dir_np, "ecocentric_noun_phrase_counts.json"),
        phrase_type="noun_phrase"
    )

    # Verbs
    count_occurrences(
        neutral_verbs,
        aggregated_files,
        os.path.join(output_dir_v, "neutral_verbs_counts.json"),
        phrase_type="verbs"
    )
    count_occurrences(
        anthropocentric_verbs,
        aggregated_files,
        os.path.join(output_dir_v, "anthropocentric_verbs_counts.json"),
        phrase_type="verbs"
    )
    count_occurrences(
        ecocentric_verbs,
        aggregated_files,
        os.path.join(output_dir_v, "ecocentric_verbs_counts.json"),
        phrase_type="verbs"
    )


# Call the function to process all counts
process_all()


"""# Sort and save rankings

## Aggregated
"""

import os
import json


def sort_noun_phrase_counts(input_files, output_directory):
    try:
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        for category, file_path in input_files.items():
            # Read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Sort by the anthropocentric_count field in descending order
            sorted_data = sorted(data, key=lambda x: x.get(f"{category}_count", 0), reverse=True)

            # Save the sorted data to the output directory
            output_file = os.path.join(output_directory, f"{category}_ranked.json")
            with open(output_file, 'w') as file:
                json.dump(sorted_data, file, indent=4)

            print(f"Sorted file saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Specify the input files and output directory
input_files_np = {
    "neutral": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/nouns_count/neutral_noun_phrase_counts.json",
    "anthropocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/nouns_count/anthropocentric_noun_phrase_counts.json",
    "ecocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/nouns_count/ecocentric_noun_phrase_counts.json",
}

input_files_v = {
    "neutral": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/verbs_count/neutral_verbs_counts.json",
    "anthropocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/verbs_count/anthropocentric_verbs_counts.json",
    "ecocentric": "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/verbs_count/ecocentric_verbs_counts.json",
}
output_directory_np = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/rankings/noun_phrases"
output_directory_v = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/rankings/verbs"

# Run the sorting and saving
sort_noun_phrase_counts(input_files_np, output_directory_np)
sort_noun_phrase_counts(input_files_v, output_directory_v)




"""## Draw histogram of frequencies"""

import json
import matplotlib.pyplot as plt
import numpy as np

# ngram = "unigrams"
ngram = "bigrams"
# type_cmp = "neutral_anth"
type_cmp = "neutral_eco"

filename = f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/words_stats/{ngram}/{experiment_name}_{type_cmp}.json'

# Load the JSON data from the file into a Python dictionary
data = {}
with open(filename, 'r') as file:
    data = json.load(file)

keys_to_delete = [key for key in data if "  " in key or key.isdigit() or key == " "]

# Delete the identified keys
for key in keys_to_delete:
    del data[key]

# Prepare data for plotting
labels = list(data.keys())
count_1 = [data[key]["count_in_neutral"] for key in labels]

if type_cmp == "neutral_anth":
    count_2 = [data[key]["count_in_anthropocentric"] for key in labels]
else:
    count_2 = [data[key]["count_in_ecocentric"] for key in labels]

x = np.arange(len(labels))  # the label locations

# Set up the width of the bars
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, count_1, width, label='Neutral Prompt Answers', color='cornflowerblue')
if type_cmp == "neutral_anth":
    rects2 = ax.bar(x + width / 2, count_2, width, label='Anthropocentric Prompt Answers', color='lightsalmon')
else:
    rects2 = ax.bar(x + width / 2, count_2, width, label='Ecocentric Prompt Answers', color='lightgreen')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel(ngram)
ax.set_title(f'Counts of {ngram} Co-Occurrences in Different Prompts Answers')
ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.xticks(rotation=90)
ax.legend()


# Add a function to attach a label above each bar
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
fig.set_size_inches(10, 6.5)
fig.tight_layout()
fig.savefig(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/graphs/{ngram}/hist/{experiment_name}_{type_cmp}.png')
# Display the plot
# plt.show()

"""# Histograms for aggregated

## Nouns
"""

import os
import json
import matplotlib.pyplot as plt
import spacy

# Load spaCy model for processing text
nlp = spacy.load("en_core_web_sm")

# Directories for input and output
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/rankings/noun_phrases"
output_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/histograms/noun_phrases"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Categories to process
categories = ["neutral", "anthropocentric", "ecocentric"]


# Function to create and save a histogram
def create_histogram(title, noun_phrases, counts, output_file):
    plt.figure(figsize=(10, 6))
    plt.bar(noun_phrases, counts, alpha=0.7)
    plt.title(title)
    plt.xlabel("Noun Phrases")
    plt.ylabel("Frequencies")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


# Function to lemmatize, deduplicate, and sort noun phrases by frequency
def lemmatize_deduplicate_and_sort(noun_phrases, counts):
    lemma_to_count = {}
    for phrase, count in zip(noun_phrases, counts):
        lemma = nlp(phrase.lower())[0].lemma_
        if lemma in lemma_to_count:
            lemma_to_count[lemma] += count
        else:
            lemma_to_count[lemma] = count
    # Sort by frequency in descending order
    sorted_items = sorted(lemma_to_count.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items], [item[1] for item in sorted_items]


# Process each category
for category in categories:
    input_file = os.path.join(input_dir, f"{category}_ranked.json")
    output_file = os.path.join(output_dir, f"{category}_histogram.png")

    # Load the JSON file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Filter noun phrases with a frequency of at least 30
    filtered_data = [item for item in data if item[f"{category}_count"] >= 30 and item["noun_phrase"] != "co"]

    # Extract noun phrases and their counts for the filtered data
    noun_phrases = [item["noun_phrase"] for item in filtered_data]
    counts = [item[f"{category}_count"] for item in filtered_data]

    # Lemmatize, deduplicate, and sort noun phrases by frequency
    unique_phrases, unique_counts = lemmatize_deduplicate_and_sort(noun_phrases, counts)

    # Create and save the histogram
    create_histogram(
        f"Frequencies of NP on {category.capitalize()} Prompts (Aggregated)",
        unique_phrases,
        unique_counts,
        output_file
    )

    print(f"Histogram for {category} saved at {output_file}")

"""## Verbs"""

import os
import json
import matplotlib.pyplot as plt
import spacy

# Load spaCy model for processing text
nlp = spacy.load("en_core_web_sm")

# Directories for input and output
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/rankings/verbs"
output_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/histograms/verbs"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Categories to process
categories = ["neutral", "anthropocentric", "ecocentric"]


# Function to create and save a histogram
def create_histogram(title, verbs, counts, output_file):
    plt.figure(figsize=(10, 6))
    plt.bar(verbs, counts, alpha=0.7)
    plt.title(title)
    plt.xlabel("Verbs")
    plt.ylabel("Frequencies")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


# Function to lemmatize, deduplicate, and sort verbs by frequency
def lemmatize_deduplicate_and_sort(verbs, counts):
    lemma_to_count = {}
    for verb, count in zip(verbs, counts):
        lemma = nlp(verb.lower())[0].lemma_
        if lemma not in ["co", "is", "are"]:  # Exclude specific words
            if lemma in lemma_to_count:
                lemma_to_count[lemma] += count
            else:
                lemma_to_count[lemma] = count
    # Sort by frequency in descending order
    sorted_items = sorted(lemma_to_count.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_items], [item[1] for item in sorted_items]


# Process each category
for category in categories:
    input_file = os.path.join(input_dir, f"{category}_ranked.json")
    output_file = os.path.join(output_dir, f"{category}_histogram.png")

    # Load the JSON file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Filter verbs with a frequency of at least 30
    filtered_data = [item for item in data if item[f"{category}_count"] >= 20]

    # Extract verbs and their counts for the filtered data
    verbs = [item["verbs"] for item in filtered_data]
    counts = [item[f"{category}_count"] for item in filtered_data]

    # Lemmatize, deduplicate, and sort verbs by frequency
    unique_verbs, unique_counts = lemmatize_deduplicate_and_sort(verbs, counts)

    # Create and save the histogram
    create_histogram(
        f"Frequencies of Verbs on {category.capitalize()} Prompts (Aggregated)",
        unique_verbs,
        unique_counts,
        output_file
    )

    print(f"Histogram for {category} saved at {output_file}")

import os
import spacy
from collections import Counter
import json

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load('en_core_web_sm')

# Define file paths
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs"
output_file = os.path.join(input_dir, "verb_frequencies.json")
files = {
    "ecocentric": os.path.join(input_dir, "ecocentric_outputs.txt"),
    "anthropocentric": os.path.join(input_dir, "anthropocentric_outputs.txt"),
    "neutral": os.path.join(input_dir, "neutral_outputs.txt"),
}

# Combine and lemmatize verbs
all_verbs = ecocentric_verbs | anthropocentric_verbs | neutral_verbs
lemmatized_verbs = set([nlp(verb)[0].lemma_ for verb in all_verbs])


# Function to read text files
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


# Function to lemmatize text and count verb frequencies
def count_verbs(text, verbs):
    doc = nlp(text)
    verb_frequencies = Counter(token.lemma_ for token in doc if token.lemma_ in verbs)
    return verb_frequencies


# Analyze files
results = {}
for file_type, file_path in files.items():
    print(f"Processing {file_type.upper()} file...")
    text = read_text_file(file_path)
    frequencies = count_verbs(text, lemmatized_verbs)
    results[file_type] = dict(sorted(frequencies.items(), key=lambda x: x[1], reverse=True))

# Save results to JSON
with open(output_file, 'w') as file:
    json.dump(results, file, indent=4)

print(f"Verb frequencies saved to {output_file}")

# Print results
for file_type, frequencies in results.items():
    print(f"\nVerb frequencies in {file_type.upper()} file:")
    for verb, count in frequencies.items():
        if count >= 10:
            print(f"{verb}: {count}")

import matplotlib.pyplot as plt
import numpy as np

# Combine relevant verbs
relevant_verbs_selection = set(
    {'disrupt', 'impact', 'supply', 'mitigate', 'pet', 'respect', 'support', 'protect', 'help', 'contribute', 'sustain',
     'live', 'regulate', 'purify', 'cause', 'adapt', 'maintain', 'balance', 'provide', 'serve', 'domesticate', 'breed',
     'benefit', 'raise', 'thrive', 'offer'})

# Filter verbs with frequency >= 30 and present in relevant lists
filtered_verbs = {}
for verb in relevant_verbs_selection:
    counts = {
        "ecocentric": results.get("ecocentric", {}).get(verb, 0),
        "anthropocentric": results.get("anthropocentric", {}).get(verb, 0),
        "neutral": results.get("neutral", {}).get(verb, 0),
    }
    if max(counts.values()) >= 0:
        filtered_verbs[verb] = counts

# Sort verbs by anthropocentric frequency (descending)
sorted_verbs = sorted(filtered_verbs.keys(), key=lambda v: filtered_verbs[v]["anthropocentric"], reverse=True)

# Prepare data for plotting
verbs = sorted_verbs
ecocentric_counts = [filtered_verbs[verb]["ecocentric"] for verb in verbs]
anthropocentric_counts = [filtered_verbs[verb]["anthropocentric"] for verb in verbs]
neutral_counts = [filtered_verbs[verb]["neutral"] for verb in verbs]

# Bar positions
x = np.arange(len(verbs))
width = 0.25

# Plot histogram
plt.figure(figsize=(15, 8))
plt.bar(x - width, ecocentric_counts, width, label='Ecocentric', color='#2E8B57', alpha=0.8)  # Sea green
plt.bar(x, anthropocentric_counts, width, label='Anthropocentric', color='#8B0000', alpha=0.8)  # Dark red
plt.bar(x + width, neutral_counts, width, label='Neutral', color='#A9A9A9', alpha=0.8)  # Dim grey

# Formatting the plot
plt.xlabel('Verbs', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.title('Verb Frequency Comparison Across Categories', fontsize=16)
plt.xticks(x, verbs, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# Save the plot
output_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/histograms/verbs"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "selected_verb_frequencies_histogram.png")
plt.savefig(output_path)

print(f"Histogram saved to: {output_path}")
print((relevant_verbs_selection))

"""# Venn

## Aggregated on word split
"""

import os
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Paths to aggregated output files
neutral_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/neutral_outputs.txt"
anthropocentric_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/anthropocentric_outputs.txt"
ecocentric_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/ecocentric_outputs.txt"


# Load words from each file

def load_words(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        words = set(content.split())  # Split content into unique words
    return words


neutral_words = load_words(neutral_file)
anthropocentric_words = load_words(anthropocentric_file)
ecocentric_words = load_words(ecocentric_file)

# Create a Venn diagram
plt.figure(figsize=(10, 8))
venn = venn3(
    subsets=(
        neutral_words,
        anthropocentric_words,
        ecocentric_words
    ),
    set_labels=("Neutral", "Anthropocentric", "Ecocentric")
)

plt.title("Intersection of Words across Categories")
output_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/venn/venn_diagram_words.png"
plt.savefig(output_file)
plt.close()

print(f"Venn diagram saved at {output_file}")

"""## Venn aggregated on lemmas"""

import os
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import spacy

# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm")

# Paths to aggregated output files
neutral_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/neutral_outputs.txt"
anthropocentric_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/anthropocentric_outputs.txt"
ecocentric_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/ecocentric_outputs.txt"


# Load and lemmatize words from each file
def load_and_lemmatize_words(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        words = content.split()  # Split content into words
        lemmatized_words = {token.lemma_ for token in nlp(" ".join(words)) if token.is_alpha}  # Lemmatize and filter
    return lemmatized_words


neutral_words = load_and_lemmatize_words(neutral_file)
anthropocentric_words = load_and_lemmatize_words(anthropocentric_file)
ecocentric_words = load_and_lemmatize_words(ecocentric_file)

# Create a Venn diagram
plt.figure(figsize=(10, 8))
venn = venn3(
    subsets=(
        neutral_words,
        anthropocentric_words,
        ecocentric_words
    ),
    set_labels=("Neutral", "Anthropocentric", "Ecocentric")
)

plt.title("Intersection of Lemmatized Words across Categories")
output_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/venn/venn_diagram_lemmatized_words.png"
plt.savefig(output_file)
plt.close()

print(f"Venn diagram saved at {output_file}")

# Categorized lists
farm_animals = [
    'what_are_animals_for',
    'what_are_animals_good_for',
    'pigs_are',
    'provide_a_description_of_chickens',
    'provide_a_description_of_cows',
    'provide_a_description_of_fishes',
    'horses_are'
]

pets_animals = [
    'dogs_are',
]

natural_entities = [
    'what_is_the_soil_for',
    'what_is_the_soil_good_for',
    'what_are_mountains_good_for',
    'what_are_the_negative_effects_of_climate_change',
    'what_are_the_negative_effects_of_climate_change_on_humans',
    'what_are_the_negative_effects_of_climate_change_on_non_human_entities',
    'provide_a_description_of_trees',
    'provide_a_description_of_soil',
    'provide_a_description_of_mountains',
    'sea_is',
    'rivers_are'
]

"""## Venn on NP Only"""

import os
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Create a Venn diagram
plt.figure(figsize=(10, 8))
venn = venn3(
    subsets=(
        neutral_noun_phrases,
        anthropocentric_noun_phrases,
        ecocentric_noun_phrases
    ),
    set_labels=("Neutral", "Anthropocentric", "Ecocentric")
)

plt.title("Intersection of Noun Phrases Across Neutral, Anthropocentric and Ecocentric")
output_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/venn/venn_diagram_noun_phrases.png"
plt.savefig(output_file)
plt.close()

print(f"Venn diagram saved at {output_file}")

import os
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Create a Venn diagram
plt.figure(figsize=(10, 8))
venn = venn3(
    subsets=(
        neutral_verbs,
        anthropocentric_verbs,
        ecocentric_verbs
    ),
    set_labels=("Neutral", "Anthropocentric", "Ecocentric")
)

plt.title("Intersection of Verbs Across Neutral, Anthropocentric and Ecocentric")
output_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/venn/venn_diagram_verbs.png"
plt.savefig(output_file)
plt.close()

print(f"Venn diagram saved at {output_file}")

import matplotlib.pyplot as plt
from matplotlib_venn import venn3


def create_venn(doc1, doc2, doc3, labels, compute_bigrams=False):
    doc1 = doc1.replace('\n', '')
    doc2 = doc2.replace('\n', '')
    doc2 = doc2.replace('\n', '')

    # Step 1: Tokenize, lemmatize, and remove stopwords and punctuation
    tokens1 = [token.lemma_.lower() for token in nlp(doc1) if not token.is_stop and not token.is_punct]
    tokens2 = [token.lemma_.lower() for token in nlp(doc2) if not token.is_stop and not token.is_punct]
    tokens3 = [token.lemma_.lower() for token in nlp(doc3) if not token.is_stop and not token.is_punct]

    # Step 2: Generate bigrams using NLTK
    if compute_bigrams:
        tokens1 = [' '.join(bigram) for bigram in bigrams(tokens1)]
        tokens2 = [' '.join(bigram) for bigram in bigrams(tokens2)]
        tokens3 = [' '.join(bigram) for bigram in bigrams(tokens3)]

    # Convert bigrams to sets
    set1 = set(tokens1)
    set2 = set(tokens2)
    set3 = set(tokens3)

    fig = plt.figure(figsize=(8, 8))
    venn_diagram = venn3([set1, set2, set3], set_labels=labels)
    plt.title('Overlapping Words in Neutral, Anthropocentric and Ecocentric Prompt Answers')
    colors = ["cornflowerblue", "lightsalmon", "lightgreen"]

    # Setting colors for each circle in the Venn diagram
    venn_diagram.get_patch_by_id('100').set_color(colors[0])
    venn_diagram.get_patch_by_id('010').set_color(colors[1])
    venn_diagram.get_patch_by_id('001').set_color(colors[2])
    # Display the plot
    if compute_bigrams:
        ngram = "bigrams"
    else:
        ngram = "unigrams"
    fig.tight_layout()
    fig.savefig(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/graphs/{ngram}/venn/{experiment_name}.png')
    # plt.show()


# Load the JSON file
with open(f'/content/drive/MyDrive/Anthropocentric_Bias/gpt/output/{experiment_name}.json', 'r') as file:
    data = json.load(file)

create_venn(data['neutral_prompt'], data['anthropocentric_prompt'], data['ecocentric_prompt'],
            ['neutral', 'anthropocentric', 'ecocentric'], True)
create_venn(data['neutral_prompt'], data['anthropocentric_prompt'], data['ecocentric_prompt'],
            ['neutral', 'anthropocentric', 'ecocentric'], False)

"""## Venn on Categories"""

import os
import json
from collections import Counter
from matplotlib_venn import venn3
import matplotlib.pyplot as plt
import spacy

# Load spaCy model for processing text
nlp = spacy.load("en_core_web_sm")

# Paths
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/output"
output_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/category_aggregated/graphs/venn"
os.makedirs(output_dir, exist_ok=True)

# Categorized lists
farm_animals = [
    'what_are_animals_for',
    'what_are_animals_good_for',
    'pigs_are',
    'provide_a_description_of_chickens',
    'provide_a_description_of_cows',
    'provide_a_description_of_fishes',
    'horses_are'
]

pets_animals = [
    'dogs_are',
]

natural_entities = [
    'what_is_the_soil_for',
    'what_is_the_soil_good_for',
    'what_are_mountains_good_for',
    'what_are_the_negative_effects_of_climate_change',
    'what_are_the_negative_effects_of_climate_change_on_humans',
    'what_are_the_negative_effects_of_climate_change_on_non_human_entities',
    'provide_a_description_of_trees',
    'provide_a_description_of_soil',
    'provide_a_description_of_mountains',
    'sea_is',
    'rivers_are'
]


# Function to process text into lemmas, removing stopwords and punctuation
def process_text(text):
    doc = nlp(text)
    return {token.lemma_ for token in doc if not token.is_stop and token.is_alpha}


# Function to aggregate data from JSON files
def aggregate_category_data(file_list):
    eco_data, antro_data, neutral_data = set(), set(), set()

    for file_name in file_list:
        file_path = os.path.join(input_dir, f"{file_name}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)

                eco_prompt = data.get("ecocentric_prompt", "")
                antro_prompt = data.get("anthropocentric_prompt", "")
                neutral_prompt = data.get("neutral_prompt", "")

                if isinstance(eco_prompt, str):
                    eco_data.update(process_text(eco_prompt))

                if isinstance(antro_prompt, str):
                    antro_data.update(process_text(antro_prompt))

                if isinstance(neutral_prompt, str):
                    neutral_data.update(process_text(neutral_prompt))

    return eco_data, antro_data, neutral_data


# Function to create and save a Venn diagram
def create_and_save_venn(category_name, eco_data, antro_data, neutral_data):
    plt.figure(figsize=(10, 8))
    venn = venn3(
        [neutral_data, antro_data, eco_data],
        ("Neutral", "Anthropocentric", "Ecocentric")
    )
    plt.title(f"Venn Diagram for {category_name.capitalize()} Category")
    output_file = os.path.join(output_dir, f"{category_name}_venn_diagram.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Venn diagram saved for {category_name} at {output_file}")


# Process categories
categories = {
    "farm_animals": farm_animals,
    "pets_animals": pets_animals,
    "natural_entities": natural_entities
}

for category_name, file_list in categories.items():
    eco_data, antro_data, neutral_data = aggregate_category_data(file_list)
    create_and_save_venn(category_name, eco_data, antro_data, neutral_data)

"""## Venn on glossary frequencies"""

import os
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Paths
input_file = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/anthropoc_glossary_np_occurrences.json"
output_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/graphs/venn"
os.makedirs(output_dir, exist_ok=True)

# Load the data
with open(input_file, "r") as file:
    data = json.load(file)

# Prepare sets for each category
neutral_set = {item["noun_phrase"] for item in data if item["neutral_occ"] > 0}
anthropocentric_set = {item["noun_phrase"] for item in data if item["anthropocentric_occ"] > 0}
ecocentric_set = {item["noun_phrase"] for item in data if item["ecocentric_occ"] > 0}

# Create a Venn diagram
plt.figure(figsize=(10, 8))
venn = venn3(
    [neutral_set, anthropocentric_set, ecocentric_set],
    set_labels=("Neutral", "Anthropocentric", "Ecocentric")
)
plt.title("Venn Diagram of Noun Phrase Occurrences Across Categories")

# Save the Venn diagram
output_file = os.path.join(output_dir, "noun_phrase_venn_diagram_glossary.png")
plt.savefig(output_file)
plt.close()

print(f"Venn diagram saved at {output_file}")

import os
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Paths
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs"
glossary_file = os.path.join(input_dir, "anthropoc_glossary_NP_cleaned.txt")
output_dir = os.path.join(input_dir, "graphs/venn/anthrop_glossary_venn")
os.makedirs(output_dir, exist_ok=True)

# Aggregated output files
files = {
    "ecocentric": os.path.join(input_dir, "ecocentric_outputs.txt"),
    "anthropocentric": os.path.join(input_dir, "anthropocentric_outputs.txt"),
    "neutral": os.path.join(input_dir, "neutral_outputs.txt"),
}

# Load the glossary
with open(glossary_file, "r") as file:
    glossary_words = set(eval(file.read()))  # Load as a Python list and convert to set for fast lookup


# Function to read words from a file
def load_words(file_path):
    with open(file_path, "r") as file:
        content = file.read().lower()  # Lowercase for consistent matching
        words = set(content.split())  # Split into unique words
    return words


# Create Venn diagrams
for category, file_path in files.items():
    category_words = load_words(file_path)  # Load words from the category file

    # Create a Venn diagram
    plt.figure(figsize=(8, 6))
    venn = venn2(
        subsets=(category_words, glossary_words),
        set_labels=(f"{category.capitalize()} Words", "Anthropocentric Glossary")
    )
    plt.title(f"Intersection of {category.capitalize()} Words and ")

    # Save the Venn diagram
    output_file = os.path.join(output_dir, f"{category}_glossary_venn.png")
    plt.savefig(output_file)
    plt.close()

    print(f"Venn diagram for {category} saved at {output_file}")

"""## Venn for category (lemmatized)"""

import os
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import spacy

# Load spaCy model for lemmatization and stopword removal
nlp = spacy.load("en_core_web_sm")

# Paths
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs"
glossary_file = os.path.join(input_dir, "anthropoc_glossary_NP_cleaned.txt")
output_dir = os.path.join(input_dir, "graphs/venn/anthrop_glossary_venn/camera_ready_fix/")
os.makedirs(output_dir, exist_ok=True)

# Aggregated output files
files = {
    "ecocentric": os.path.join(input_dir, "ecocentric_outputs.txt"),
    "anthropocentric": os.path.join(input_dir, "anthropocentric_outputs.txt"),
    "neutral": os.path.join(input_dir, "neutral_outputs.txt"),
}


# Function to preprocess text: lemmatize, remove stopwords, and punctuation
def preprocess_text(words):
    processed_words = set()
    for word in words:
        doc = nlp(word.lower())
        for token in doc:
            if not token.is_stop and token.is_alpha:  # Remove stopwords and punctuation
                processed_words.add(token.lemma_)
    return processed_words


# Load and preprocess the glossary
with open(glossary_file, "r") as file:
    glossary_words = set(eval(file.read()))  # Load as a Python list
    glossary_words = preprocess_text(glossary_words)


# Function to read and preprocess words from a file
def load_and_preprocess_words(file_path):
    with open(file_path, "r") as file:
        content = file.read().lower()  # Lowercase for consistent matching
        words = set(content.split())  # Split into unique words
    return preprocess_text(words)


# Create Venn diagrams
for category, file_path in files.items():
    category_words = load_and_preprocess_words(file_path)  # Load and preprocess words

    # Create a Venn diagram
    plt.figure(figsize=(8, 6))
    venn = venn2(
        subsets=(category_words, glossary_words),
        set_labels=(f"Words Generated From {category.capitalize()} Prompt", "Anthropocentric Glossary")
    )
    plt.title(f"Lemmatized Word Overlap: {category.capitalize()} Prompt & Anthropocentric Glossary",
              fontdict={"fontsize": 12, "fontweight": "bold"})
    # Save the Venn diagram
    output_file = os.path.join(output_dir, f"{category}_glossary_venn_lemmas.png")
    plt.savefig(output_file)
    plt.close()

    print(f"Venn diagram for {category} saved at {output_file}")

"""## Weighted"""

import os
import spacy
from collections import Counter
from matplotlib_venn import venn2
import matplotlib.pyplot as plt
import ast

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load('en_core_web_sm')

# Define file paths
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs"
glossary_file = os.path.join(input_dir, "anthropoc_glossary_NP_cleaned.txt")
output_dir = os.path.join(input_dir, "graphs/venn/anthrop_glossary_venn/weighted")

# Define input files
files = {
    "ecocentric": os.path.join(input_dir, "ecocentric_outputs.txt"),
    "anthropocentric": os.path.join(input_dir, "anthropocentric_outputs.txt"),
    "neutral": os.path.join(input_dir, "neutral_outputs.txt"),
}

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)


def read_glossary_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return ast.literal_eval(content)


def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def lemmatize_text(text):
    max_length = len(text)
    chunk_size = 1000000
    lemmatized_words = Counter()

    for i in range(0, max_length, chunk_size):
        chunk = text[i:i + chunk_size]
        doc = nlp(chunk)
        chunk_words = [token.lemma_.lower() for token in doc
                       if token.is_alpha and not token.is_stop]
        lemmatized_words.update(chunk_words)

    return lemmatized_words


def create_venn_diagram(text_words, glossary_words, output_path, file_type):
    text_set = set(text_words.keys())
    total_text_words = sum(text_words.values())
    intersection = sum(text_words[word] for word in text_set & glossary_words)

    only_text = total_text_words - intersection
    only_glossary = len(glossary_words - text_set)

    plt.figure(figsize=(10, 10))
    venn2(subsets=(only_text, only_glossary, intersection),
          set_labels=(f'{file_type.capitalize()} Words\n(Total: {total_text_words:,})',
                      f'Anthropocentric Glossary Words\n(Total: {len(glossary_words):,})'))
    plt.title(f'Word Overlap between {file_type.capitalize()} Outputs and Anthropocentric Glossary\n' +
              f'(Intersection: {intersection:,} occurrences)')

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    return {
        'total_words': total_text_words,
        'unique_words': len(text_set),
        'intersection_occurrences': intersection,
        'intersection_unique': len(text_set & glossary_words)
    }


def save_word_lists(text_words, glossary_words, output_dir, file_type):
    text_words_path = os.path.join(output_dir, f'{file_type}_words_frequencies.txt')
    with open(text_words_path, 'w') as f:
        f.write("word\tfrequency\n")
        for word, freq in sorted(text_words.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{word}\t{freq}\n")

    overlap_path = os.path.join(output_dir, f'{file_type}_overlapping_words.txt')
    with open(overlap_path, 'w') as f:
        overlap = set(text_words.keys()) & glossary_words
        f.write("word\tfrequency\n")
        for word in sorted(overlap):
            f.write(f"{word}\t{text_words[word]}\n")


# Read and process glossary
print("Processing glossary...")
glossary_words = set(lemmatize_text(' '.join(read_glossary_file(glossary_file))).keys())

# Save glossary words
glossary_path = os.path.join(output_dir, 'glossary_lemmatized.txt')
with open(glossary_path, 'w') as f:
    f.write("word\n")
    for word in sorted(glossary_words):
        f.write(f"{word}\n")

# Process each file separately
for file_type, file_path in files.items():
    print(f"\nProcessing {file_type} file...")

    text_content = read_text_file(file_path)
    text_word_frequencies = lemmatize_text(text_content)

    output_path = os.path.join(output_dir, f'word_overlap_venn_weighted_{file_type}.png')
    stats = create_venn_diagram(text_word_frequencies, glossary_words, output_path, file_type)

    save_word_lists(text_word_frequencies, glossary_words, output_dir, file_type)

    print(f"\nDetailed Statistics for {file_type}:")
    print(f"Total words (including duplicates): {stats['total_words']:,}")
    print(f"Unique words: {stats['unique_words']:,}")
    print(f"Words in anthropocentric glossary: {len(glossary_words):,}")
    print(f"Unique words in both: {stats['intersection_unique']:,}")
    print(f"Total occurrences of glossary words: {stats['intersection_occurrences']:,}")

    print(f"\nTop overlapping words with frequencies for {file_type} (top 10):")
    overlapping_words = set(text_word_frequencies.keys()) & glossary_words
    sorted_overlap = sorted([(word, text_word_frequencies[word])
                             for word in overlapping_words],
                            key=lambda x: x[1],
                            reverse=True)[:10]
    for word, freq in sorted_overlap:
        print(f"{word}: {freq}")

"""# Anthrop glossary frequencies"""

import os
import json

# Directories
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs"
output_file = os.path.join(input_dir, "anthropoc_glossary_np_occurrences.json")
glossary_file = os.path.join(input_dir, "anthropoc glossary_NP_cleaned.txt")

# Aggregated output files
neutral_file = os.path.join(input_dir, "neutral_outputs.txt")
anthropocentric_file = os.path.join(input_dir, "anthropocentric_outputs.txt")
ecocentric_file = os.path.join(input_dir, "ecocentric_outputs.txt")


# Function to count occurrences of words in a file
def count_occurrences(words, file_path):
    with open(file_path, "r") as file:
        content = file.read().lower()  # Convert content to lowercase for case-insensitive matching
    return {word: content.count(word) for word in words}


# Load the glossary
with open(glossary_file, "r") as file:
    glossary_words = eval(file.read())  # Load the list from the file (assuming valid Python list syntax)

# Convert glossary words to lowercase for consistent matching
glossary_words = [word.lower() for word in glossary_words]

# Count occurrences in each file
neutral_occurrences = count_occurrences(glossary_words, neutral_file)
anthropocentric_occurrences = count_occurrences(glossary_words, anthropocentric_file)
ecocentric_occurrences = count_occurrences(glossary_words, ecocentric_file)

# Aggregate the results
results = []
for word in glossary_words:
    results.append({
        "noun_phrase": word,
        "neutral_occ": neutral_occurrences[word],
        "anthropocentric_occ": anthropocentric_occurrences[word],
        "ecocentric_occ": ecocentric_occurrences[word],
    })

# Save the results to a JSON file
with open(output_file, "w") as file:
    json.dump(results, file, indent=4)

print(f"Occurrences of noun phrases saved to {output_file}")

import os
import spacy
from collections import Counter
import ast
import pandas as pd

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load('en_core_web_sm')

# Define file paths
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs"
glossary_file = os.path.join(input_dir, "anthropoc_glossary_NP_cleaned.txt")
output_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/aggregated_outputs/statistics"
os.makedirs(output_dir, exist_ok=True)

# Define input files
files = {
    "ecocentric": os.path.join(input_dir, "ecocentric_outputs.txt"),
    "anthropocentric": os.path.join(input_dir, "anthropocentric_outputs.txt"),
    "neutral": os.path.join(input_dir, "neutral_outputs.txt"),
}


def read_glossary_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return ast.literal_eval(content)


def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def lemmatize_text(text):
    max_length = len(text)
    chunk_size = 1000000
    lemmatized_words = Counter()

    for i in range(0, max_length, chunk_size):
        chunk = text[i:i + chunk_size]
        doc = nlp(chunk)
        chunk_words = [token.lemma_.lower() for token in doc
                       if token.is_alpha and not token.is_stop]
        lemmatized_words.update(chunk_words)

    return lemmatized_words


# Read and process glossary
print("Processing glossary...")
glossary_words = set(lemmatize_text(' '.join(read_glossary_file(glossary_file))).keys())

# Collect results for each file
results = []

# Process each file
for file_type, file_path in files.items():
    print(f"\n{'=' * 50}")
    print(f"Statistics for {file_type.upper()} outputs:")
    print('=' * 50)

    # Process text file
    text_content = read_text_file(file_path)
    word_frequencies = lemmatize_text(text_content)

    # Total lemmas (with duplicates)
    total_lemmas = sum(word_frequencies.values())
    print(f"\nTotal lemmas (with duplicates): {total_lemmas:,}")

    # Unique lemmas
    unique_lemmas = len(word_frequencies)
    print(f"\nTotal unique lemmas: {unique_lemmas:,}")

    # Glossary words overlap (without repetitions)
    overlap_unique = len(set(word_frequencies.keys()) & glossary_words)
    print(f"\nGlossary words appearing in text (without repetitions): {overlap_unique:,}")

    # Glossary words overlap (with repetitions)
    overlap_total = sum(word_frequencies[word] for word in glossary_words if word in word_frequencies)
    print(f"\nGlossary words appearing in text (with repetitions): {overlap_total:,}")

    # Frequencies of overlapping words
    print("\nFrequencies of overlapping words (top 10, sorted by frequency):")
    overlapping_words = [(word, word_frequencies[word])
                         for word in glossary_words
                         if word in word_frequencies]
    sorted_overlap = sorted(overlapping_words, key=lambda x: x[1], reverse=True)[:10]
    for word, freq in sorted_overlap:
        print(f"    {word}: {freq:,}")

    # Percentages of overlap
    print("\nOverlap percentages:")
    # Without repetitions (unique words)
    unique_overlap_percentage = (overlap_unique / unique_lemmas) * 100
    print(f"    Without repetitions: {unique_overlap_percentage:.2f}% of text words are from the glossary")

    # With repetitions (relative to total words)
    total_overlap_percentage = (overlap_total / total_lemmas) * 100
    print(f"    With repetitions: {total_overlap_percentage:.2f}% of text words are from the glossary")

    # Append results to list
    results.append({
        "File Type": file_type,
        "Total Lemmas (With Duplicates)": total_lemmas,
        "Unique Lemmas": unique_lemmas,
        "Overlap with Anthropocentic Glossary (No Repetitions)": overlap_unique,
        "Overlap with Anthropocentic Glossary (With Repetitions)": overlap_total,
        "Overlap % (No Repetitions)": unique_overlap_percentage,
        "Overlap % (With Repetitions)": total_overlap_percentage
    })

# Save results to an Excel file
output_file = os.path.join(output_dir, "statistics_summary.xlsx")
df = pd.DataFrame(results)
df.to_excel(output_file, index=False)
print(f"\nResults saved to {output_file}")
