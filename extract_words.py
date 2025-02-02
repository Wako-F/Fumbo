import re

# Try different encodings
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

# Clean up the text first
text = text.replace('\n', ' ')

# Load English words to filter out
english_words = set()
try:
    with open('english_words.txt', 'r') as f:
        english_words = set(word.strip().lower() for word in f)
except FileNotFoundError:
    english_words = {'light', 'learn', 'logic', 'level', 'large', 'later', 'layer', 'lease', 
                    'leave', 'ledge', 'legal', 'lemon', 'limit', 'linen', 'loose', 'lover', 
                    'lower', 'loyal', 'lusty', 'magic', 'major', 'maker', 'march', 'marks',
                    'marsh', 'mason', 'masts', 'match', 'mauve', 'means', 'medal', 'mercy',
                    'merge', 'merry', 'metal', 'micro', 'midge', 'might', 'mince', 'mirth',
                    'miser', 'mixed'}

# Process the words
word_definitions = {}

def clean_definition(definition):
    # Remove any trailing word entries
    definition = re.sub(r'\s+[a-z]+\s*(?:nm|kt|kv|kl|ki)\b.*$', '', definition)
    
    # Remove grammar notes in parentheses
    definition = re.sub(r'\(tde\)[^.;]*', '', definition)
    definition = re.sub(r'\(tdk\)[^.;]*', '', definition)
    definition = re.sub(r'\(tds\)[^.;]*', '', definition)
    definition = re.sub(r'\(tdw\)[^.;]*', '', definition)
    definition = re.sub(r'\(tdn\)[^.;]*', '', definition)
    
    # Remove other parenthetical content
    definition = re.sub(r'\([^)]+\)', '', definition)
    
    # Remove type markers and brackets
    definition = re.sub(r'\[[^\]]+\]', '', definition)
    definition = re.sub(r'\b(?:nm|kt|kv|kl|ki)\b', '', definition)
    definition = re.sub(r'ma-\s*', '', definition)  # Remove ma- prefix
    
    # Remove cross-references
    definition = re.sub(r'(?:taz|pia)\s+[a-z]+', '', definition)
    
    # Clean up any remaining markers
    definition = re.sub(r'[~\-]\s*', '', definition)
    
    return definition.strip()

# Pattern to match entries
pattern = r'\b([a-z]+(?:[\.-][a-z]+)?)\*?\s+(?:nm|kt|kv|kl|ki)\s*(?:\[[^\]]+\])?\s*(.*?)(?=\s+[a-z]+\s+(?:nm|kt|kv|kl|ki)\s|$)'
entries = re.findall(pattern, text.lower())

for word, definition in entries:
    # Clean the word
    clean_word = word.replace('.', '').replace('-', '')
    clean_word = re.sub(r'\d+$', '', clean_word)  # Remove trailing numbers
    
    # Check if it's a valid 5-letter Swahili word
    if len(clean_word) == 5 and clean_word not in english_words:
        # Clean up definition
        definition = clean_definition(definition)
        
        # Split into multiple definitions
        defs = []
        # First try numbered definitions
        numbered_matches = re.findall(r'\b\d+\s*([^.0-9]+?)(?=\b\d+|$)', definition)
        
        if numbered_matches:
            defs = [d.strip() for d in numbered_matches if d.strip()]
        else:
            # If no numbered definitions, split by periods and semicolons
            defs = [d.strip() for d in re.split('[.;]', definition) if d.strip()]
        
        # Join valid definitions
        if defs:
            final_defs = []
            for d in defs:
                d = d.strip()
                if len(d) > 1 and not d.isdigit() and not any(marker in d for marker in ['nm', 'kt', 'kv', 'kl', 'ki']):
                    final_defs.append(d)
            
            if final_defs:
                word_definitions[clean_word] = '; '.join(final_defs)

# Output the results
with open("five_letter_words.txt", "w", encoding="utf-8") as output_file:
    for word in sorted(word_definitions.keys()):
        output_file.write(f'{word} - {word_definitions[word]}\n')

print(f"Found {len(word_definitions)} five-letter Swahili words")
