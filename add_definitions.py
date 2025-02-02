import re

# Read the cleaned words
with open("five_letter_words.txt", "r", encoding="utf-8") as file:
    words = [line.strip() for line in file.readlines()]

print(f"Read {len(words)} words")

# Read kamusi.txt with different encodings
encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
for encoding in encodings:
    try:
        with open("kamusi.txt", "r", encoding=encoding) as file:
            text = file.read()
        break
    except UnicodeDecodeError:
        if encoding == encodings[-1]:
            raise
        continue

# Clean up the text
text = text.replace('\n', ' ')

# Dictionary to store word definitions
word_definitions = {}

# For each word, find its definition in kamusi.txt
for word in words:
    # Create multiple patterns to try matching
    patterns = [
        # Pattern 1: Basic word with marker
        rf'\b{re.escape(word)}\s*(?:nm|kt|kv|kl|ki)\b([^.]*?)(?=\b[a-z]+\s*(?:nm|kt|kv|kl|ki)\b|$)',
        
        # Pattern 2: Word with possible dots
        rf'\b{re.escape(".".join(word))}\s*(?:nm|kt|kv|kl|ki)\b([^.]*?)(?=\b[a-z]+\s*(?:nm|kt|kv|kl|ki)\b|$)',
        
        # Pattern 3: More relaxed pattern
        rf'\b{re.escape(word)}\b[^.]*?(?=\b[a-z]+\s*(?:nm|kt|kv|kl|ki)\b|$)',
        
        # Pattern 4: Word at start of entry
        rf'\b{re.escape(word)}\b[^.]*?(?:\.|$)'
    ]
    
    definition = "no definition found"
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            # Get the definition part
            if match.groups():
                definition = match.group(1)
            else:
                definition = match.group(0)
                
            # Clean up definition
            definition = re.sub(r'^\s*(?:nm|kt|kv|kl|ki)\s*(?:\[[^\]]+\])?\s*', '', definition)
            definition = re.sub(r'\([^)]*\)', '', definition)
            definition = definition.split(';')[0].strip()
            if definition:  # If we got a non-empty definition
                break
    
    word_definitions[word] = definition

# Write words with definitions back to file
with open("five_letter_words.txt", "w", encoding="utf-8") as file:
    for word in sorted(word_definitions.keys()):
        file.write(f"{word} - {word_definitions[word]}\n")

print(f"Added definitions for {len(word_definitions)} words") 