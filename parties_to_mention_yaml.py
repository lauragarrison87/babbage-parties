import csv

template = """\
- model: parties.mention
  fields:
    party: {party}
    guest: {name}
    source: {source}

"""

with open("parties.csv", newline="", encoding="utf8") as f:
    next(f)
    csvfile = csv.reader(f)
    for line in csvfile:
        line = [ x.strip() for x in line ]

        party,_,qid,_,source,_,_ = line
        if qid == "Unknown":
            qid = 'Q24238356'
        qid = int(qid[1:])
        print(template.format(party=party, name=qid, source=source))
        
        


