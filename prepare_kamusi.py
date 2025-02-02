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
    Remove any leading line numbers of the form "number|".
    """
    return re.sub(r"^\d+\|", "", content, flags=re.MULTILINE)

def normalize_whitespace(content):
    """
    Replace multiple whitespace characters (including newlines) with a single space.
    """
    return re.sub(r'\s+', ' ', content).strip()

def insert_newlines_before_marker(content):
    """
    Insert a newline before any occurrence of the marker (Kar) variants.
    For example, this matches "(Kar)" or "Kar)".
    """
    return re.sub(r'(?<!\n)(\(?Kar\)?\s*)', r'\n\1', content)

def insert_newlines_before_headword(content):
    """
    Insert a newline before a headword based on a heuristic:
    Look for a headword (letters, digits, dot, or asterisk) not preceded by a newline,
    which is then followed by one or more spaces before "nm" or "kt" (common definition markers).
    
    Example match: "abud.u1* kt" will get a newline inserted before "abud.u1*".
    """
    pattern = r'(?<!\n)([a-zA-Z][a-zA-Z0-9\.\*]+)\s+(?=(nm|kt)\b)'
    return re.sub(pattern, r'\n\1 ', content)

def main():
    # Read the kamusi.txt file using multiple encodings.
    content = read_file_with_encodings("kamusi.txt")
    
    # Clean the content:
    # 1. Remove any leading line numbers.
    content = clean_line_numbers(content)
    # 2. Normalize whitespace so that multiple spaces/newlines reduce to a single space.
    content = normalize_whitespace(content)
    # 3. Insert newlines before any explicit marker (e.g. "(Kar)" or "Kar)").
    content = insert_newlines_before_marker(content)
    # 4. Insert newlines before headwords when the marker is missing—
    #    a headword is defined as a token beginning with a letter which is followed (after whitespace)
    #    by "nm" or "kt".
    content = insert_newlines_before_headword(content)
    
    # Write the cleaned text to a new file.
    with open("kamusi_cleaned.txt", "w", encoding="utf-8") as outf:
        outf.write(content)
    
    print("Cleaned content saved to 'kamusi_cleaned.txt'.")

if __name__ == "__main__":
    main() 