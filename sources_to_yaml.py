import csv

template = """\
- model: parties.source
  pk: "{sid}"
  fields:
    source: "{source}"
    quote: "{quote}"
    pages: {pages}

"""

with open("sources.csv", newline="", encoding="utf8") as f:
    next(f)
    csvfile = csv.reader(f)
    for line in csvfile:
        line = [x.strip() for x in line]
        sid, source, quote, pages = line
        if not source or source == '""':
            source = sid
        if not pages:
            pages = "null"
        else:
            pages = f'"{pages}"'
        print(template.format(sid=sid, source=source, quote=quote, pages=pages))
        


