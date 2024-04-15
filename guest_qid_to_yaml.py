import csv

template = """\
- model: parties.person
  pk: {qid}
  fields:
    name: "{name}"
    presumed: {presume}

"""

with open("guest_qid.csv", newline="", encoding="utf8") as f:
    next(f)
    csvfile = csv.reader(f)
    for line in csvfile:
        try:
            name, qid, presume = line
        except ValueError:
            name, presume = line
            qid = presume
        if qid == "Unknown":
            qid = 'Q24238356' # "entity whose identity is not known"
        presume = bool(presume)
        qid = qid.strip()
        print(template.format(qid=qid, name=name, presume=presume))
        


