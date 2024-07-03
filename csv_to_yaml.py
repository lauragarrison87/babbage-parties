import csv
import sys
from json import dumps
import difflib
from textwrap import dedent, wrap

class Skip(Exception):
    pass

def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = "parties.csv"

    with open(filename, newline="", encoding="utf8") as f:
        # skip 2 header lines
        next(f)
        next(f)
        csvfile = csv.reader(f)
        for line in csvfile:
            line = [ x.strip() for x in line ]
            pid,name,qid,presumed,sid,pages,quote,source,_ = line
        
            try:
                pid = print_party(pid)
                qid = print_person(qid, name)
                sids = print_source(sid,pages,quote,source)
                for sid in sids:
                    print_mention(pid,qid,sid,presumed)

            except Skip:
                continue

            except AssertionError as e:
                sys.stderr.write(f"Consistency Error: {e}\n")
                sys.exit(1)


pid_seen = set()
def print_party(pid):
    if not pid:
        raise Skip

    if pid in pid_seen:
        sys.stderr.write(f"Duplicate party: {pid}\n")
        return pid

    pid_seen.add(pid)

    date = pid.split('-')
    match date:
        case [y,m,d]:
            year, month, day = int(y), int(m), int(d)
        case [y,m]:
            year, month, day = int(y), int(m), "null"
        case [y]:
            try:
                year = int(y)
            except ValueError:
                year = "null"
            month, day = "null", "null"

    print(dedent(
        f"""\
        - model: parties.party
          pk: {pid}
          fields:
            year: {year}
            month: {month}
            day: {day}

        """
    ))
    return pid


qid_seen = {}
def print_person(qid, name):
    if not qid:
        raise Skip

    if qid == "Unknown":
        qid = 'Q24238356' # "entity whose identity is not known"
    
    if qid in qid_seen:
        assert qid_seen[qid] == name, f"{qid}: {qid_seen[qid]} =/= {name}"
        sys.stderr.write(f"Duplicate person: {qid} {name}\n")
        return qid
    else:
        qid_seen[qid] = name

    print(dedent(
        f"""\
        - model: parties.person
          pk: {qid}
          fields:
            name: "{name}"

        """
    ))
    return qid


def print_source(sids,pages,quotes,sources):
    sids = sids.split('@')
    sids = [ x.strip() for x in sids ]

    if len(sids) > 1:
        pages = pages.split('@')
        pages = [ x.strip() for x in pages ]
    
        quotes = quotes.split('@')
        quotes = [ x.strip() for x in quotes ]
    
        sources = sources.split('@')
        sources = [ x.strip() for x in sources ]
        if len(sources) == 1 and sids[0][:-1] == sids[1][:-1]:
            # assume same source
            sources = sources * len(sids)

        assert len(sids) == len(sources) == len(pages) == len(quotes), f"Unequal lengths {sids}"

    else:
        pages = [pages]
        quotes = [quotes]
        sources = [sources]

    for sid,page,quote,source in zip(sids,pages,quotes,sources):
        bid = sid[:-1] if sid[-1] in "abcdefghijklmnopqrstuvwxyz" else sid
        print_one_book(bid, source)
        print_one_source(sid, bid, page, quote)

    return sids

bid_seen = {}
def print_one_book(bid, source):
    if bid in bid_seen:
        if not source:
            source = bid_seen[bid]
        assert bid_seen[bid] == source, f"{bid}: {bid_seen[bid]} =/= {source}"
        sys.stderr.write(f"Duplicate book: {bid}\n")
        return
    else:
        bid_seen[bid] = source

    print(dedent(
        f"""\
        - model: parties.book
          pk: {bid}
          fields:
            citation: {dumps(source, ensure_ascii=False)}
        """
    ))

sid_seen = {}
def print_one_source(sid, bid, page, quote):
    args = (bid,page,quote)
    if sid in sid_seen:
        if sid_seen[sid] != args:
            for a,b in zip(sid_seen[sid], args):
                if a == b:
                    continue
                else:
                    sys.stderr.write(f"====== INCONSISTENCY in {sid} ======\n\n")
                    sys.stderr.writelines(
                        difflib.ndiff(
                            [f"{i}\n" for i in wrap(a,40)],
                            [f"{i}\n" for i in wrap(b,40)],
                        )
                    )
                    sys.stderr.write('\n')
                    sys.exit(1)

            sys.stderr.write(f"{sid}: {sid_seen[sid]} =/= {args}\n")
        else:
            sys.stderr.write(f"Duplicate source: {sid} {args}\n")
            return
    else:
        sid_seen[sid] = args

    print(dedent(
        f"""\
        - model: parties.source
          pk: {sid}
          fields:
            book: {bid}
            quote: {dumps(quote, ensure_ascii=False)}
            pages: {page}

        """
    ))


def print_mention(pid,qid,sid,presumed):
    print(dedent(
        f"""\
        - model: parties.mention
          fields:
            party: {pid}
            guest: {qid}
            source: {sid}
            presumed: {bool(presumed)}

        """
    ))



if __name__ == "__main__":
    main()
