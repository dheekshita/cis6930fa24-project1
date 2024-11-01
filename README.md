# cis6930fa24 -- Project 1

Name: Dheekshita Neella

# Project Description
This project identifies sensitive information from multiple text files and censors it. It makes use of SpaCy, NLTK and Regular Expressions to censor data like Names, Dates, Phone Numbers, Addresses, and content related to a given concept. It also generates statistics based on the redacted content.


# How to install
pipenv install

## How to run
pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones --address\
                    --concept '<concept>' \
                    --output 'files/' \
                    --stats stderr|stdout

The Flags names, dates, phones, address and concept are optional and can be modified based on the requirement.

### Examples
pipenv run python redactor.py --input '*.txt' \
                    --names --dates\
                    --concept 'house' \
                    --output 'files/' \
                    --stats stderr

pipenv run python redactor.py --input '*.txt' \
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr

pipenv run python redactor.py --input '*.txt' \
                    --names --phones\
                    --concept 'house' --concept 'kids'\
                    --output 'files/' \
                    --stats stderr

## Functions
censor(text, entities) - It replaces characters in the identified sensitive information with '█'. It takes in original text(text) and the content containing sensitive information(entities) and replaces the characters in entities with █. Returns censored text.

identify_dates(text), identify_address(text), identify_names(text), identify_phones(text) - These functions identifies the Dates, Addresses, Names, Phones respectively. They take in the original text and returns list of information that is identified as sensitive. To extract dates, addresses and phone numbers, Regular expressions are used. To identify names, SpaCy is used and Regular Expressions are used for some special cases.

identify_concept(text, concepts) - This function censors sentences based on the concept(s) given thorugh input. It takes in original text and the concept(s) given during execution and returns text with sentences censored based on the gvien concept(s).

censor_file(input_file, output_dir, flags, concepts) - This function applies the censor function to the given input files and saves the censored output files. It takes in the input files, folder to save the output file, flags given during the execution thereby censoring only the entities in the flags given during runtime, and concepts given, if any. It returns censored entities that are in a dictionary.

stats(censored_entities, stat, output_dir) - This function gets the statistics of the censored entities and saves them to a file. It takes in the dictionary of censored entities, dict for maintaining stats and the folder to save the output stats file.

## Test cases
test_dates - Tests if the dates are being identified correctly. It gives a string containing different formats of dates to the identify_dates() funtion and checks if all types of formats are being identified properly.

test_concept - Tests if the sentences related to a concept is extracted. 
It gives a string containing sentences which include the concept, it's synonyms and sentence without any related word. It checks if the sentences containing the concept and it's synonyms are being redacted and if the sentences not related to the concept are not being redacted.

test_names - Tests if the names are extracted correctly. It gives a string containing Names in different formats, one with first and last name, one with underscore and one with only first name. Then it checks if all of them are identified.

test_address - Tests if addresses are being extracted correctly. It gives a string containing multiple address formats and checks if all of them are extracted.

test_phones - Tests for the correct extraction of phone numbers. It gives string containing phone numbers of different formats and checks if they are being identified properly.

## Bugs and Assumptions
1. This project does not redact names conataining hyphens, or other special characters, excluding '_'. If the logic for including names with special characters is added, other info is being censored unnecessarily.
2. Some Address formats, like the ones containing only the City name are not being extracted properly.
3. In the context of concept based redaction, it is assumed that sentences regarding the concept contain synonym words to the given word. 
4. While redaction of phone numbers, the character '(' at the start of the phone number is not being censored.

## Parameters applied to flags
1. Dates - Checking multiple formats of dates and days with Regular Expressions like mm/dd/yyyy; Nov 6; April 9, 2019; Mon; Thursday
2. Names - Using SpaCy to recognize the names and using Regular Expressions to handle special cases like names with underscores and name sin emails.
3. Phones - Phone numbers in xxx-xxx-xxxx, (xxx) xxx-xxxx and xxxxxxxxxx formats
4. Address - Considers addresses in formats like 123 Maple Street and Springfield, IL 62701.
5. Concepts - NLTK is used to find synonymous words to the given concepts and each word is checked if they are in the synonyms list. If there, it redacts the whole sentence containing the synonymous or the concept word.

## Additional Notes
1. Whitespaces are included while censoring the text as otherwise one can know how many lettered words are present in a redacted text and this makes it easier for someone to guess the censored text. Makes the whole process less effective.
2. How concepts are redacted - The sentences containing concept word or synonyms of the word are consored.
3. STATS file - This file contains no. of Names, Dates, Phone Number and Addresses that are censored.
