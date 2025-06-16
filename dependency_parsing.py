"""# Dependancy parsing"""

import spacy
import json


def parse_dependency(json_data, experiment_name):
    # Load the spaCy model (English in this case)
    nlp = spacy.load("en_core_web_sm")

    # Initialize a dictionary to store the parsed results
    parsed_results = {}

    # Iterate through each prompt type and parse the text
    for key, text in json_data.items():
        doc = nlp(text)
        parsed_results[key] = {
            "tokens": [
                {
                    "text": token.text,
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep": token.dep_,
                    "head": token.head.text
                }
                for token in doc
            ],
            "noun_phrases": [chunk.text for chunk in doc.noun_chunks]
        }

    return parsed_results


import os
import json

# Directory containing the JSON files
input_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/output"
output_dir = "/content/drive/MyDrive/Anthropocentric_Bias/gpt/dependancy_parsing"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Iterate over each JSON file in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".json"):  # Process only JSON files
        experiment_name = os.path.splitext(file_name)[0]
        input_file_path = os.path.join(input_dir, file_name)

        # Read the JSON file
        with open(input_file_path, 'r') as file:
            data = json.load(file)

        # Parse the dependency
        parsed_output = parse_dependency(data, experiment_name)

        # Save the parsed output
        output_file = os.path.join(output_dir, f"{experiment_name}_dep_pars.json")
        with open(output_file, "w") as f:
            json.dump(parsed_output, f, indent=4)

        print(f"Processed and saved: {output_file}")

"""## Heads frequencies"""

# Import required libraries
import os
import json
from collections import defaultdict, Counter
from typing import Dict, List
from pathlib import Path
import spacy
from IPython.display import display, JSON

# Initialize spaCy and configuration
nlp = spacy.load("en_core_web_sm")

# Configure paths
input_dir = Path("/content/drive/MyDrive/Anthropocentric_Bias/gpt/dependency_parsing")
output_dir = Path("/content/drive/MyDrive/Anthropocentric_Bias/gpt/dependency_parsing/frequencies")
output_dir.mkdir(exist_ok=True)

# Define target words
words_to_match = [
    "animals", "soil", "mountains", "chickens", "horses", "wolves",
    "fishes", "cows", "trees", "pigs", "dogs", "sea", "rivers"
]

# Create lemmatization cache
lemma_cache = {}


def get_lemma(word: str) -> str:
    """Get lemma with caching for better performance."""
    if word not in lemma_cache:
        lemma_cache[word] = nlp(word.lower())[0].lemma_
    return lemma_cache[word]


# Pre-compute lemmas for matching
lemma_dict = {get_lemma(word): word for word in words_to_match}

# Initialize data structure for token processing
token_data = {
    'neutral': defaultdict(Counter),
    'anthropocentric': defaultdict(Counter),
    'ecocentric': defaultdict(Counter)
}


def process_file(file_path: Path) -> None:
    """Process a single JSON file and extract token information."""
    try:
        with file_path.open('r') as f:
            data = json.load(f)

        for category in token_data.keys():
            category_key = f"{category}_prompt"
            tokens = data.get(category_key, {}).get("tokens", [])

            for token in tokens:
                text_lemma = get_lemma(token["text"])
                if text_lemma in lemma_dict:
                    original_word = lemma_dict[text_lemma]
                    token_data[category][original_word][token["head"]] += 1

    except json.JSONDecodeError:
        print(f"Error reading JSON file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")


# Process all files
print("Processing files...")
for file_path in input_dir.glob("*.json"):
    process_file(file_path)
    print(f"Processed: {file_path.name}")

# Generate output data with sorted frequencies
output_data = {}
for category in token_data.keys():
    category_data = []
    for word in words_to_match:
        # Get frequencies and sort them
        frequencies = token_data[category][word]
        sorted_frequencies = dict(sorted(frequencies.items(), key=lambda x: (-x[1], x[0])))

        category_data.append({
            "prompt_word": word,
            f"list_of_{category}_heads": list(sorted_frequencies.keys()),
            f"{category}_heads_occurrences": sorted_frequencies
        })
    output_data[category] = category_data

# Save results
for category, data in output_data.items():
    output_file = output_dir / f"{category}_head_frequencies.json"
    with output_file.open('w') as f:
        json.dump(data, f, indent=4)
    print(f"\nSaved {category} data to {output_file}")
