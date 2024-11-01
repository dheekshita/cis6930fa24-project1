import argparse
import os
import re
import spacy
import glob
import sys
import nltk
from nltk.corpus import wordnet as wn
from collections import defaultdict

nlp = spacy.load("en_core_web_md")
nltk.download('wordnet', quiet=True)

DATES = [
    r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)',
    r'\b(?:Monday|Tueday|Wednesday|Thursday|Friday|Saturday|Sunday)',
    r'\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}\b',
    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{1,2}(?:,\s*\d{4})?\b',
    r'(?<=\s)\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}(?=\s)'
]
PHONE_NUMBERS = r'\b(?:\+?\d{1,3}[-. ]?)?(?:\(?\d{3}\)?[-. ]?)\d{3}[-. ]?\d{4}\b(?!\.\w+@|\.\w{2,})'
ADDRESS = [
    r'(?i)\b([A-Za-z\s]+),\s*([A-Z]{2})\s*(\d{5})(-\d{4})?\b',
    r'(?i)\b(\d{1,5}\s+[A-Za-z0-9\s.]+(?:Avenue|Street|Road|Blvd|Lane|Dr|Court|Way|Broadway|Center)\b)',
]


def censor(text, entities):
    k = '█'
    for i in sorted(entities, key=len, reverse=True):
        escapes = re.escape(i)
        text = re.sub(r'\b' + escapes + r'\b', k * len(i), text)
    return text

def identify_dates(text):
    dates = []
    for pattern in DATES:
        dates.extend(re.findall(pattern, text))
    return dates

def identify_phones(text):
    return re.findall(PHONE_NUMBERS, text)


def identify_address(text):
    address = []
    for pattern in ADDRESS:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                city, state, zip_code, zip_suffix = match
                formatted_address = f"{city.strip()}, {state} {zip_code}{zip_suffix if zip_suffix else ''}"
                address.append(formatted_address)
            else:
                address.append(match.strip())
    return address

def identify_names(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON" and not re.fullmatch(r'_+', ent.text)]
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9.-]+\.)*com\b', text)
    underscore_names = re.findall(r'\b\w+_\w+\b', text)
    header_pattern = re.findall(r'From:\s*["\']?(\w+),?\s+(\w+)["\']?\s*<.*?>', text)
    for first, last in header_pattern:
        names.extend([first, last])
    return list(set(names)) + emails + underscore_names

def identify_concept(text, concepts):
    doc = nlp(text)
    redacted = []
    synonyms = set()

    for concept_word in concepts:
        synonyms.add(concept_word.lower())
        for synset in wn.synsets(concept_word):
            for lemma in synset.lemmas():
                synonym = lemma.name().replace('_', ' ')
                synonyms.add(synonym.lower())

    for sentence in doc.sents:
        if any(synonym in sentence.text.lower() for synonym in synonyms):
            redacted.append("█" * len(sentence.text))
        else:
            redacted.append(sentence.text)
    
    return " ".join(redacted)



def censor_file(input_file, output_dir, flags, concepts):
    censored_entities = defaultdict(list)

    with open(input_file, 'r') as f:
        text = f.read()

    if flags['names']:
        names = identify_names(text)
        censored_entities['names'] = names
        text = censor(text, names)

    if flags['dates']:
        dates = identify_dates(text)
        censored_entities['dates'] = dates
        text = censor(text, dates)

    if flags['phones']:
        phones = identify_phones(text)
        censored_entities['phones'] = phones
        text = censor(text, phones)

    if flags['address']:
        addresses = identify_address(text)
        censored_entities['addresses'] = addresses
        text = censor(text, addresses)

    if concepts:
        text = identify_concept(text, concepts)

    output_file = os.path.join(output_dir, os.path.basename(input_file) + '.censored')
    with open(output_file, 'w') as f:
        f.write(text)

    return censored_entities

def stats(censored_entities, stat, output_dir):
    for entity_type, items in censored_entities.items():
        stat[entity_type] += len(items)
    
    # Write stats to a file
    stats_output = os.path.join(output_dir, 'stats.txt')
    with open(stats_output, 'w') as f:
        for entity_type, count in stat.items():
            f.write(f"{entity_type}: {count}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default = '*.txt')
    parser.add_argument('--output', type=str, default = 'files/')
    parser.add_argument('--names', action='store_true')
    parser.add_argument('--dates', action='store_true')
    parser.add_argument('--phones', action='store_true')
    parser.add_argument('--address', action='store_true')
    parser.add_argument('--concept', action='append')
    parser.add_argument('--stats', choices=['stderr', 'stdout'])

    args = parser.parse_args()

    flags = {
        'names': args.names,
        'dates': args.dates,
        'phones': args.phones,
        'address': args.address,
    }

    concepts = args.concept if args.concept else []
    os.makedirs(args.output, exist_ok=True)
    input_files = glob.glob(args.input)
    stat = defaultdict(int)

    for input_file in input_files:
        censored_entities = censor_file(input_file, args.output, flags, concepts)
        stats(censored_entities, stat, args.output)

    
if __name__ == "__main__":
    main()