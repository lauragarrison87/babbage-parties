import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import time

def main(file, rows=None):
    parties, unique_qids = load_data(file, rows)
    for qid in unique_qids['qid']:
        # Check if qid is correctly formatted
        if not str(qid).strip().startswith('Q') or not str(qid).strip()[1:].isdigit():
            continue
        character_info = fetch_character_info(qid, parties)  # Pass parties as an argument
        print_character_sheet(character_info, unique_qids, parties)
        # Sleep for 1 second to avoid rate limiting
        time.sleep(1)

def load_data(file, rows=None):
    parties = pd.read_csv(file, nrows=rows)
    unique_qids = pd.DataFrame(parties['qid'].unique(), columns=['qid'])
    return parties, unique_qids

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
            ?spouseLabel
            ?birthplaceLabel
            ?causeOfDeathLabel
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
            OPTIONAL {{ wd:{qid} wdt:P26 ?spouse. ?spouse rdfs:label ?spouseLabel FILTER(LANG(?spouseLabel) = "en") }}
            OPTIONAL {{ wd:{qid} wdt:P19 ?birthplace. ?birthplace rdfs:label ?birthplaceLabel FILTER(LANG(?birthplaceLabel) = "en") }}
            OPTIONAL {{ wd:{qid} wdt:P509 ?causeOfDeath. ?causeOfDeath rdfs:label ?causeOfDeathLabel FILTER(LANG(?causeOfDeathLabel) = "en") }}
            FILTER(LANG(?label) = "en" && LANG(?description) = "en")
        }}
        GROUP BY ?label ?description ?genderLabel ?birthName ?birthDate ?deathDate ?occupationLabel ?nationalityLabel ?spouseLabel ?birthplaceLabel ?causeOfDeathLabel
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

def fetch_character_info(qid, parties):
    results = fetch_data(qid)
    character_info = {
        'qid': qid,
        'label': results['results']['bindings'][0].get('label', {'value': None})['value'],
        'description': results['results']['bindings'][0].get('description', {'value': None})['value'],
        'gender': results['results']['bindings'][0].get('genderLabel', {'value': None})['value'],
        'aliases': results['results']['bindings'][0].get('aliases', {'value': None})['value'],
        'birthName': results['results']['bindings'][0].get('birthName', {'value': None})['value'],
        'birthYear': results['results']['bindings'][0].get('birthDate', {'value': None})['value'],
        'deathYear': results['results']['bindings'][0].get('deathDate', {'value': None})['value'],
        'occupation': results['results']['bindings'][0].get('occupationLabel', {'value': None})['value'],
        'nationality': results['results']['bindings'][0].get('nationalityLabel', {'value': None})['value'],
        'spouse': results['results']['bindings'][0].get('spouseLabel', {'value': None})['value'],
        'birthplace': results['results']['bindings'][0].get('birthplaceLabel', {'value': None})['value'],
        'causeOfDeath': results['results']['bindings'][0].get('causeOfDeathLabel', {'value': None})['value'],
 
        'dates': parties[parties['qid'] == qid]['date'].tolist(),
        'quotes': parties[parties['qid'] == qid]['quote'].tolist(),  # Add a comma at the end of this line
    }
    if character_info['birthYear'] is not None:
        character_info['birthYear'] = character_info['birthYear'].split('-')[0]
    if character_info['deathYear'] is not None:
        character_info['deathYear'] = character_info['deathYear'].split('-')[0]
    return character_info

def other_guests(parties, qid, dates):
    other_guests_set = set()
    for date in dates:
        other_guests_on_date = parties[(parties['date'] == date) & (parties['qid'] != qid)]['qid']
        other_guests_set.update(other_guests_on_date)
    return list(other_guests_set)

def generate_character_info(character_info, unique_qids):
    pronoun_subjective = check_pronoun(character_info['gender'], 'subjective')
    pronoun_possessive = check_pronoun(character_info['gender'], 'possessive')
    spouse = check_none(character_info['spouse'])
    
    output = f"\n--------------------------------------------------------\n"
    output += f"CHARACTER SHEET FOR: {character_info['label']} ({character_info['birthYear']}-{character_info['deathYear']})\n"
    output += "--------------------------------------------------------\n"
    output += f"Short description: {character_info['description']}\n\n"
    output += f"{check_none(character_info['label'])} was a {check_none(character_info['gender'])} {check_none(character_info['occupation'])} from {check_none(character_info['nationality'])}. {pronoun_subjective} was also known as {check_none(character_info['aliases'])}."
    
    if character_info['birthName']:
        output += f" {pronoun_possessive} birth name was {character_info['birthName']}. "
    
    if character_info['birthplace']:
        output += f"{pronoun_subjective} was born in {check_none(character_info['birthplace'])}. "
    
    if character_info['spouse']:
        guest_status = ", who was also a guest." if spouse in unique_qids['qid'].tolist() else ""
        output += f"{pronoun_subjective} was married to {spouse}{guest_status}. "

    if character_info['causeOfDeath']:
        output += f"{pronoun_subjective} died of {character_info['causeOfDeath']}.\n"
    
    output += f"\n"
    return output

def other_guests(parties, qid, dates):
    other_guests_list = []
    for date in dates:
        other_guests_on_date = parties[(parties['date'] == date) & (parties['qid'] != qid)]
        for _, guest_row in other_guests_on_date.iterrows():
            guest_qid = guest_row['qid']
            guest_description = fetch_character_info(guest_qid, parties)['description']
            other_guests_list.append((guest_qid, guest_description))
    return other_guests_list

def generate_soiree_info(character_info, parties):  
    output = "\nSoirées attended:\n"
    output += "------------------"
    for date, quote in zip(character_info['dates'], character_info['quotes']):
        other_guests_list = other_guests(parties, character_info['qid'], [date])
        output += f"\n{date}: \"{quote}\"\n\nOther known guests that evening:\n"
        if other_guests_list:
            for guest_qid, guest_description in other_guests_list:
                guest_info = fetch_character_info(guest_qid, parties)
                output += f"- {guest_info['label']}: {guest_description}\n"
        else:
            output += "No other guests\n"
    return output

def print_character_sheet(character_info, unique_qids, parties):
    character_info_str = generate_character_info(character_info, unique_qids)
    soiree_info_str = generate_soiree_info(character_info, parties)
    
    with open('character_sheets.txt', 'a') as f:  # Open the file in append mode
        f.write(character_info_str)
        f.write(soiree_info_str)  # Write the soiree info to the file
        f.write("\n\n")  # Add a newline to separate different character sheets

    #print(character_info_str)
    #print(soiree_info_str)


if __name__ == "__main__":
    
    file='parties.csv'
    #rows=10
    rows=None # Uncomment this line to read the entire file
    main(file,rows)




