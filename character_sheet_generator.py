import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import time

# Load the first five rows from parties.csv
df = pd.read_csv('parties.csv', skiprows=range(1, 30), nrows=20)

# Create a DataFrame with unique qids
unique_qids = pd.DataFrame(df['qid'].unique(), columns=['qid'])

def construct_query(qid):
    # Check if qid is correctly formatted
    if not str(qid).strip().startswith('Q') or not str(qid).strip()[1:].isdigit():
        raise Exception("The qid is not correctly formatted.")
        return None
    
    query=f"""
        SELECT 
            ?label 
            ?description
            ?genderLabel 
            ?birthName 
            ?birthDate 
            ?deathDate 
            ?occupationLabel 
            ?nationalityLabel 
            (GROUP_CONCAT(DISTINCT ?alias; SEPARATOR=", ") AS ?aliases)
        WHERE {{
            wd:{qid} rdfs:label ?label.
            wd:{qid} schema:description ?description.
            OPTIONAL {{ wd:{qid} skos:altLabel ?alias FILTER(LANG(?alias) = "en") }}
            OPTIONAL {{ wd:{qid} wdt:P21 ?gender. ?gender rdfs:label ?genderLabel FILTER(LANG(?genderLabel) = "en") }}
            OPTIONAL {{ wd:{qid} wdt:P1477 ?birthName. }}
            OPTIONAL {{ wd:{qid} wdt:P569 ?birthDate. }}
            OPTIONAL {{ wd:{qid} wdt:P570 ?deathDate. }}
            OPTIONAL {{ wd:{qid} wdt:P106 ?occupation. ?occupation rdfs:label ?occupationLabel FILTER(LANG(?occupationLabel) = "en") }}
            OPTIONAL {{ wd:{qid} wdt:P27 ?nationality. ?nationality rdfs:label ?nationalityLabel FILTER(LANG(?nationalityLabel) = "en") }}
            FILTER(LANG(?label) = "en" && LANG(?description) = "en")
        }}
        GROUP BY ?label ?description ?genderLabel ?birthName ?birthDate ?deathDate ?occupationLabel ?nationalityLabel
    """
    return query

# Function to fetch data from Wikidata
def fetch_data(qid):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(construct_query(qid))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def check_none(value):
    return '' if value is None else value

def check_pronoun(gender, pronoun_type):
    if pronoun_type == 'subjective':
        return "He" if gender == "male" else "She" if gender == "female" else "They"
    elif pronoun_type == 'possessive':
        return "His" if gender == "male" else "Her" if gender == "female" else "Their"

def fetch_character_info(qid):
    results = fetch_data(qid)
    character_info = {
        'label': results['results']['bindings'][0].get('label', {'value': None})['value'],
        'description': results['results']['bindings'][0].get('description', {'value': None})['value'],
        'gender': results['results']['bindings'][0].get('genderLabel', {'value': None})['value'],
        'aliases': results['results']['bindings'][0].get('aliases', {'value': None})['value'],
        'birthName': results['results']['bindings'][0].get('birthName', {'value': None})['value'],
        'birthYear': results['results']['bindings'][0].get('birthDate', {'value': None})['value'],
        'deathYear': results['results']['bindings'][0].get('deathDate', {'value': None})['value'],
        'occupation': results['results']['bindings'][0].get('occupationLabel', {'value': None})['value'],
        'nationality': results['results']['bindings'][0].get('nationalityLabel', {'value': None})['value'],
        'dates': df[df['qid'] == qid]['date'].tolist(),
        'quotes': df[df['qid'] == qid]['quote'].tolist()
    }
    if character_info['birthYear'] is not None:
        character_info['birthYear'] = character_info['birthYear'].split('-')[0]
    if character_info['deathYear'] is not None:
        character_info['deathYear'] = character_info['deathYear'].split('-')[0]
    return character_info

def print_character_sheet(character_info):
    print(f"CHARACTER SHEET FOR: {character_info['label']} ({character_info['birthYear']}-{character_info['deathYear']})")
    print("----------------------------------")
    print(f"Short description: {character_info['description']}")
    output = f"{check_none(character_info['label'])} was a {check_none(character_info['gender'])} {check_none(character_info['occupation'])} from {check_none(character_info['nationality'])}. {check_pronoun(character_info['gender'], 'subjective')} was also known as {check_none(character_info['aliases'])}."
    if character_info['birthName']:
        output += f" {check_pronoun(character_info['gender'], 'possessive')} birth name was {character_info['birthName']}."
    print(output)
    print()
  
    print(f"Soirées attended:")
    print("---------------")
    for date, quote in zip(character_info['dates'], character_info['quotes']):
        print(f"{date}: \"{quote}\"")
        print()
    print()

# Process each unique qid
for qid in unique_qids['qid']:
    # Check if qid is correctly formatted
    if not str(qid).strip().startswith('Q') or not str(qid).strip()[1:].isdigit():
        continue
    # Fetch character info and print character sheet
    character_info = fetch_character_info(qid)
    print_character_sheet(character_info)
    # Sleep for 1 second to avoid rate limiting
    time.sleep(1)




