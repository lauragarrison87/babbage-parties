import csv

template = """\
- model: parties.source
  pk: "{sid}"
  fields:
    source: "{source}"
    quote: "{quote}"
    pages: "{pages}"

"""

with open("sources.csv", newline="", encoding="utf8") as f:
    next(f)
    csvfile = csv.reader(f)
    for line in csvfile:
        line = [x.strip() for x in line]
        sid, source, quote, pages = line
        if not source or source == '""':
            source = sid
        print(template.format(sid=sid, source=source, quote=quote, pages=pages))
        


