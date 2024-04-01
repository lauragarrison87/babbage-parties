"""
Script to clean up data about guests who attended Babbage's soirées in the 1830s and 1840s.
Data was first converted from a word doc to the parties_orig.csv file.

This script creates a new dataframe called parties and exports it to csv and excel formats. The 
dataframe contains the following fields (columns):

- date: date - sometimes exact, sometimes just year or year-month. Needs formatting somehow.
- guest: Name of the guest. 
            question: Names of the aristocracy are complex - for instance, should
            Annabella Byron be listed as Lady Byron? Might need to ask a historian. Could go with 
            whatever name their Wikidata entry has as the main form.
- qid: Wikidata identifier for the guest
- sourceID: unique identifier for the source, matches sourceID in sources.csv
- certainty_P1480: either 'presumably' or 'stated in source'. This measures how certain we are that 
this guest attended this party. In most cases 
the source is clear, but sometimes a guest is referenced just by their family name and there are multiple
people it could refer to. P1480 is a reference to the Wikidata property P1480, and 'presumably' is one of the 
options for this property.
- sourceID: a unique identifier for the source, usually the author's family name and year of publication
- quote: the direct quote that describes the guests and the party
- pages: page numbers in the bibliographic reference - will likely be combined with 
      bibliographic info later
    
"""

import pandas as pd

# Read the CSV file containing the original data about the parties
parties = pd.read_csv('parties_orig.csv', 
                 usecols=['date', 'guest', 'sourceID', 'quote', 'pages'], 
                 dtype={'guest': str, 'sourceID': str, 'quote': str, 'pages': str})
parties['guest'] = parties['guest'].str.split(',')
parties = parties.explode('guest')
parties['guest'] = parties['guest'].str.strip()
parties = parties.sort_values('sourceID')

# Read the CSV file containing the QIDs for the guests
guests = pd.read_csv('guest_qid.csv')
#---CREATE A NEW CSV FILE WITH ONE ROW PER GUEST---#
# Merge parties and guests using the field 'guest' as the shared field and keeping all the fields in both
parties = parties.merge(guests, on='guest', how='left')
parties = parties.drop_duplicates()
#parties['certainty_P1480'] = parties['certainty_P1480'].fillna('stated in source')
parties = parties[['date', 'guest', 'qid', 'certainty_P1480', 'sourceID', 'pages', 'quote']]

#---PRINTS OUT BASIC INFO---#
num_unique_guests = len(parties['guest'].unique())
num_unique_dates = len(parties['date'].unique())
print("Number of unique Guests:", num_unique_guests)
print("Number of unique Dates:", num_unique_dates)

# Save to csv and excel files
parties.to_csv('parties.csv', index=False)
parties.to_excel('parties.xlsx', index=False)

exit()

#---SEPARATE OUT SOURCE DATA---#
# Separate out the sources and save to a new CSV file
sources = df[['sourceID', 'author_date_source', 'quote', 'pages']]
sources.to_csv('sources.csv', index=False)








