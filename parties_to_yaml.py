import csv

template = """\
- model: parties.party
  pk: {pid}
  fields:
    year: {year}
    month: {month}
    day: {day}

"""

with open("parties.csv", newline="", encoding="utf8") as f:
    next(f)
    csvfile = csv.reader(f)
    seen = set()
    for line in csvfile:
        pid = line[0].strip()
        if pid in seen:
            continue
        else:
            seen.add(pid)
        date = pid.split('-')
        match date:
            case [y,m,d]:
                print(template.format(pid=pid, year=int(y), month=int(m), day=int(d)))
            case [y,m]:
                print(template.format(pid=pid, year=int(y), month=int(m), day="null"))
            case [y]:
                print(template.format(pid=pid, year=int(y), month="null", day="null"))
        
        


