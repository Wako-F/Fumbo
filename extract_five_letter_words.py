#!/usr/bin/env python3
import re

def read_file_with_encodings(filename, encodings=['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']):
    """
    Try reading the file with the given encodings in order.
    Returns the file contents as a string if one encoding works.
    Otherwise, raises a ValueError.
    """
    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as f:
                content = f.read()
            print(f"Successfully read {filename} using encoding: {enc}")
            return content
        except UnicodeDecodeError as e:
            print(f"Failed decoding {filename} with {enc}: {e}")
    raise ValueError(f"Unable to decode file {filename} with provided encodings.")

def clean_line_numbers(content):
    """
    Remove any leading line numbers of the form "number|"
    """
    return re.sub(r"^\d+\|", "", content, flags=re.MULTILINE)

def extract_entries(content):
    """
    Extract five letter words and their definitions from the content.
    Each entry may be preceded by a line number and may contain (Kar) markers.
    """
    entries = []
    # Split into lines to handle line-by-line
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Remove line numbers at the start
        line = re.sub(r'^\d+\|', '', line)
        # Remove (Kar) markers
        line = re.sub(r'\(Kar\)', '', line)
        
        # Split into words and try to find potential headwords
        words = line.split()
        if not words:
            continue
            
        # Look at first few words as potential headwords
        # (sometimes the word might be the second item after annotations)
        for word in words[:2]:
            # Clean the word by removing annotations and punctuation
            cleaned_word = re.sub(r'\[.*?\]', '', word)  # Remove [...] annotations
            cleaned_word = re.sub(r'[^a-zA-Z]', '', cleaned_word).lower()
            
            if len(cleaned_word) == 5:
                # Get the definition (everything after the word)
                definition_start = line.find(word) + len(word)
                definition = line[definition_start:].strip()
                # Clean up the definition
                definition = re.sub(r'\[.*?\]', '', definition)  # Remove [...] annotations
                definition = definition.strip('* .')  # Remove asterisks and periods
                if definition:
                    entries.append((cleaned_word, definition))
                break  # Only take the first valid 5-letter word from each line
    
    return entries

def main():
    # Read the kamusi_cleaned.txt file using multiple encodings
    content = read_file_with_encodings("kamusi_cleaned.txt")
    
    # Extract dictionary entries
    entries = extract_entries(content)
    
    # Output results in a CSV file
    with open("five_letter_words.csv", "w", encoding="utf-8") as outf:
        outf.write("Word,Definition\n")
        for word, definition in entries:
            # Escape double quotes in the definition for CSV compliance
            clean_definition = definition.replace('"', '""')
            outf.write(f'"{word}","{clean_definition}"\n')
    
    print(f"Extracted {len(entries)} five-letter entries to 'five_letter_words.csv'.")

if __name__ == "__main__":
    main() 