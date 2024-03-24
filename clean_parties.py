"""
Script to clean up data about guests who attended Babbage's soirées in the 1830s and 1840s.
Data was first converted from a word doc to the parties_orig.csv file.

This script creates two new CSV files:
1. 'sources.csv' which contains the source information, including 
    - sourceID: a unique identifier
    - author_date_source: messy (author: year) - will probably be deleted and replaced 
      by the full bibliographic information as in a reference list
    - quote: the direct quote that describes the guests and the party
    - pages: page numbers in the bibliographic reference - will likely be combined with 
      bibliographic info
2. 'parties.csv' which contains the party information with QIDs for the guests
    - date: date - sometimes exact, sometimes just year or year-month. Needs formatting somehow.
    - guest: Name of the guest. Names of the aristocracy are complex - for instance, should
      Annabella Byron be listed as Lady Byron? Might need to ask a historian. Could go with 
      whatever name their Wikidata entry has as the main form.
    - qid: Wikidata identifier for the guest
    - sourceID: unique identifier for the source, matches sourceID in sources.csv
"""

import pandas as pd

# Read the CSV file
df = pd.read_csv('parties_orig.csv', usecols=range(6))
df['guest'] = df['guest'].str.replace(r'\s*,\s*', ',', regex=True)

#---SEPARATE OUT SOURCE DATA---#
# Separate out the sources and save to a new CSV file
sources = df[['sourceID', 'author_date_source', 'quote', 'pages']]
sources.to_csv('sources.csv', index=False)

#---CLEAN PARTY DATA---#
# Separate out just the dates, guests and SourceIDs
df1 = df[['date', 'guest', 'sourceID']]
# New line for each party-guest combination
dates_guests = df1.copy()
dates_guests['guest'] = dates_guests['guest'].str.split(',')
dates_guests = dates_guests.explode('guest')
# Remove any empty strings from the 'Guests' column
dates_guests = dates_guests[dates_guests['guest'] != '']

#---PRINTS OUT BASIC INFO---#
num_unique_guests = len(dates_guests['guest'].unique())
num_unique_dates = len(dates_guests['date'].unique())
print("Number of unique Guests:", num_unique_guests)
print("Number of unique Dates:", num_unique_dates)

#---ADD QIDS FOR GUESTS TO CONNECT TO WIKIDATA---#
guests = pd.read_csv('guest_qid.csv', usecols=range(2))
dates_guests = pd.merge(dates_guests, guests, on='guest', how='left')
dates_guests = dates_guests[['date', 'guest', 'qid', 'sourceID']]
dates_guests = dates_guests.drop_duplicates()

# Save new csv file
dates_guests.to_csv('parties.csv', index=False)






