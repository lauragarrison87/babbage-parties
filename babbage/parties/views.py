from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Person, Mention, Source, Party
import random


def index(request):
    context = {'foobar' : 'HELLO 3!!!'}
    template = loader.get_template("parties/index.html")
    return HttpResponse(template.render(context, request))

def balloon(request):
    context = {}
    template = loader.get_template("parties/balloon.html")
    return HttpResponse(template.render(context, request))

def person_list(request):
    all_people = Person.objects.order_by("name")
    template = loader.get_template("parties/person/index.html")
    context= {'all_people' : all_people}
    return HttpResponse(template.render(context, request))

def make_pronouns(gender):
    if gender == "male":
        return "he", "his", "was"
    elif gender == "female":
        return "she", "her", "was"
    else: 
        return "they", "their", "were"

def person_qid(request, qid):
    person = Person.objects.get(qid=qid)
    mentions = person.mention_set.all().select_related("party","source")
    parties_attended = set(m.party for m in mentions)
    party_list = []
    for pa in parties_attended:
        party_sources = set(m.source for m in mentions.filter(party=pa))
        other_pa_mentions = ( 
            pa.mention_set.all()
                .exclude(guest=person)
                .select_related("guest")
        )
        other_guests = set( opm.guest for opm in other_pa_mentions )
        party_list.append(
            {
                'party' : pa,
                'sources' : party_sources,
                'others' : other_guests,
            }
        )

    template = loader.get_template("parties/person/specific.html")
    subj, poss, to_be = make_pronouns(person.gender)
    context= {
        'p' : person, 
        "have_detail" : True,
        "they" : subj,
        "their" : poss,
        "were" : to_be,
        "party_list" : party_list,
        }
    return HttpResponse(template.render(context, request))


def api_balloon(request):
    all_parties = Party.objects.all()
    response = {
        'parties' : {},
    }
    for party in all_parties:
        print(party.year, party.month)
        response['parties'][party.pid] = {
                "pid" : party.pid,
                "year": party.year,
                "month": party.month if party.month else 6,
                "day": party.day if party.day else 1,
                "guests": [],
                "party_size": 0,
                "ypos": random.uniform(0.1, 0.95),
            }
    
    for m in Mention.objects.all():
        response['parties'][m.party.pid]['guests'].append(m.guest.qid)
        response['parties'][m.party.pid]["party_size"] += 1

    return JsonResponse(list(response["parties"].values()), safe=False)

###

static_party_number = {}
MAX_PARTY_NUM = 0
def generate_ypos_by_party(party):
    if not static_party_number:
        all_parties = Party.objects.all()
        for i,p in enumerate(all_parties):
            static_party_number[p] = i
        global MAX_PARTY_NUM
        MAX_PARTY_NUM = i
        

    return (static_party_number[party] + 0.5*random.random()) / MAX_PARTY_NUM



def get_visdata_by_person(request):

    all_people = Person.objects.order_by("name")
    response = {
        'people' : {},
    }

    for person in all_people:
        response["people"][person.qid] = {
            "name": person.name,
            "birthdate": person.birth if person.birth else "null",
            "deathdate": person.death if person.death else "null",
            "parties" : [],
            "personal_yval" : random.random(),
        }
        
    
    for mention in (
            Mention.objects
            .select_related("party","guest")
            .order_by("party")
        ):
        response['people'][mention.guest.qid]['parties'].append(
            {
                "year": mention.party.year,
                "month": mention.party.month if mention.party.month else 6,
                "day": mention.party.day if mention.party.day else 1,
                "ypos": response['people'][mention.guest.qid]["personal_yval"],
            }
        )
    popular_people = []
    for key, value in response["people"].items():
        print(len(value["parties"]))
        if len(value["parties"]) > 1:
            popular_people.append(value)

    print(*popular_people, sep="\n")


    # return JsonResponse(list(response["people"].values()), safe=False)
    return JsonResponse(popular_people, safe=False)
