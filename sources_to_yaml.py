import csv
import json
import sys
import difflib
from pprint import pprint
import textwrap as tw


sources_template = """\
- model: parties.source
  pk: "{sid}"
  fields:
    source: {source}
    quote: {quote}
    pages: {pages}

"""

sources_consistency = {}

with open("parties.csv", newline="", encoding="utf8") as f:
    next(f)
    next(f)
    csvfile = csv.reader(f)
    for line in csvfile:
        line = [x.strip() for x in line]
        _,_,_,_,sid,pages,quote,source,_ = line
#        sid, source, quote, pages = line
        if not sid:
            continue

        if not source or source == '""':
            source = sources_consistency.get(sid, (_,_,sid))[2]

        if not pages or pages == "/":
            pages = "null"
        else:
            pages = f'"{pages}"'

        
        current_data = (pages,quote,source)
        try:
            prev_data = sources_consistency[sid]
            assert prev_data == current_data
        except KeyError:
            sources_consistency[sid] = current_data
            print(sources_template.format(
                sid=sid, 
                source=json.dumps(source, ensure_ascii=False), 
                quote=json.dumps(quote, ensure_ascii=False), 
                pages=pages
            ))
        except AssertionError:
            for a,b in zip(prev_data, current_data):
                if a == b:
                    continue
                else:
                    sys.stderr.writelines(
                        difflib.ndiff(
                            [f"{i}\n" for i in tw.wrap(a,40)],
                            [f"{i}\n" for i in tw.wrap(b,40)],
                        )
                    )
                    sys.stderr.write('\n')
                    raise

        
        


