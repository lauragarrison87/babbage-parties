import csv

template = """\
- model: parties.mention
  fields:
    party: {party}
    guest: {name}
    source: {source}
    presumed: {presumed}

"""

with open("parties.csv", newline="", encoding="utf8") as f:
    next(f)
    next(f)
    csvfile = csv.reader(f)
    seen = set()
    for line in csvfile:
        line = [ x.strip() for x in line ]
        party,_,qid,presumed,source,_,_,_,_ = line
        if not qid:
            continue
        if qid == "Unknown":
            qid = 'Q24238356'
        qid = qid.strip()
        if (party,qid,presumed,source) in seen:
            assert False, f"{(party,qid,presumed,source)}"
        else:
            seen.add((party,qid,presumed,source))
        print(template.format(party=party, name=qid, source=source, presumed=bool(presumed)))
        
        


