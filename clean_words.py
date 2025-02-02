import csv
import re
from collections import defaultdict

# Dictionary to store word -> list of definitions
word_definitions = defaultdict(list)

# Expanded list of prefixes to remove
prefixes = [
    'kt', 'ma-', 'wa-', 'i-/zi-', 'wa- a-/wa-', 'i-/zi-', 'u-/i', 'u-/i-',  'mi-', '1', 'nm', 'kv', 'kl', 'ku', 'ki', 'ks', 'kn', 'kh', 
    'tde', 'tdk', 'tdn', 'tds', 'tdw', 'tden', 'tdew', 'vi-', 'a-wa-', 'a-/wa-', 'u-', 'a-/wa', 'vy-', 'vy-vi-', 'ya-', 'mia-', 'a-', 'mi -',
]

def clean_definition(definition):
    """Clean a single definition by removing prefixes and unnecessary punctuation"""
    definition = definition.strip()
    
    # First pass: remove prefixes at start of string
    for prefix in prefixes:
        if definition.lower().startswith(prefix + ' '):
            definition = definition[len(prefix):].strip()
    
    # Second pass: remove prefixes within the string
    for prefix in prefixes:
        definition = re.sub(rf'\b{prefix}\b', '', definition, flags=re.IGNORECASE)
    
    # Clean up extra spaces and punctuation
    definition = re.sub(r'\s+', ' ', definition)  # normalize spaces
    definition = definition.strip('.- ;,')
    return definition

# First read into text file for inspection
with open("five_letter_words.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    
    # Write raw entries to text file for inspection
    with open("words_raw.txt", "w", encoding="utf-8") as outf:
        for row in reader:
            if len(row) == 2:
                word, definition = row
                outf.write(f"{word}: {definition}\n")

# Now process the text file
with open("words_raw.txt", "r", encoding="utf-8") as file:
    for line in file:
        if ':' in line:
            word, definition = line.split(':', 1)
            word = word.strip()
            
            # Split definition if it contains multiple parts
            parts = re.split(r'[;,]\s*', definition)
            
            # Clean each part and add if not empty
            for part in parts:
                cleaned_def = clean_definition(part)
                if cleaned_def:  # Only add if we have a definition
                    word_definitions[word].append(cleaned_def)

# Write cleaned definitions back to text file for inspection
with open("words_cleaned.txt", "w", encoding="utf-8") as file:
    for word, definitions in sorted(word_definitions.items()):
        combined_def = "; ".join(definitions)
        file.write(f"{word}: {combined_def}\n")

# Finally, write back to CSV
with open("five_letter_words.csv", "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Word", "Definition"])
    
    for word, definitions in sorted(word_definitions.items()):
        combined_def = "; ".join(definitions)
        writer.writerow([word, combined_def])

print(f"Processed {len(word_definitions)} words")
print("Check words_raw.txt and words_cleaned.txt to verify the cleaning process") 