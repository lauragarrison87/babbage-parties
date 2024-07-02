import csv

template = """\
- model: parties.person
  pk: {qid}
  fields:
    name: "{name}"

"""

with open("parties.csv", newline="", encoding="utf8") as f:
    next(f)
    next(f)
    csvfile = csv.reader(f)
    seen = {}
    for line in csvfile:
        _,name,qid,_,_,_,_,_,_ = line
        if not qid:
            continue
        name = name.strip()
        if qid == "Unknown":
            qid = 'Q24238356' # "entity whose identity is not known"
        qid = qid.strip()
        if qid in seen:
            assert name == seen[qid], f"{qid} {name} == {seen[qid]}"
            continue
        else:
            seen[qid] = name
            print(template.format(qid=qid, name=name))



