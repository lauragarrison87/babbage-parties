import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import sqlite3
import time

class Skip(Exception):
    pass

# Function to fetch data from Wikidata
def fetch_data(qid):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(construct_query(qid))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def main():
    DB_PATH = 'babbage/db.sqlite3'

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    qids = cur.execute("SELECT qid,birth,death,gender FROM parties_person")

    for qid,birth,death,gender in qids.fetchall():
        # print(qid,birth,death,gender)
        if birth or death or gender:
            continue
        try:
            character_info = fetch_character_info(qid)
        except Skip as e:
            print(f"=== {e}")
            continue

        print("===")
        print(character_info)
        
        cur.execute("UPDATE parties_person SET (birth, death, aliases, birthname, birthplace, deathcause, gender, nationality, occupation) = (?,?,?,?,?,?,?,?,?) WHERE qid = ?", (
                character_info["birthYear"], 
                character_info["deathYear"], 
                character_info["aliases"], 
                character_info["birthName"], 
                character_info["birthplace"], 
                character_info["causeOfDeath"], 
                character_info["gender"], 
                character_info["nationality"], 
                character_info["occupation"], 
                qid
            )
        )

        con.commit()

        time.sleep(5)



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


def fetch_character_info(qid):
    results = fetch_data(qid)
    if not results['results']['bindings']:
        raise Skip(f"No info for {qid}.")
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
    }
    if character_info['birthYear'] is not None:
        character_info['birthYear'] = character_info['birthYear'].split('-')[0]
    if character_info['deathYear'] is not None:
        character_info['deathYear'] = character_info['deathYear'].split('-')[0]
    return character_info


if __name__ == "__main__":
    main()
