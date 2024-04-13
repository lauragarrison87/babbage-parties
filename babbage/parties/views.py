from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Person, Guest, Source, Party
import random


def index(request):
    context = {'foobar' : 'HELLO 3!!!'}
    template = loader.get_template("parties/index.html")
    return HttpResponse(template.render(context, request))

def person_list(request):
    all_people = Person.objects.order_by("name")
    template = loader.get_template("parties/person/index.html")
    context= {'all_people' : all_people}
    return HttpResponse(template.render(context, request))

def make_pronouns(gender):
    if gender == "male":
        return "he", "his"
    elif gender == "female":
        return "she", "her"
    else: 
        return "they", "their"

def person_qid(request, qid):
    person = Person.objects.get(qid=qid)
    was_guest_at = Guest.objects.filter(name=person)

    soirees = Guest.objects.select_related("party","source").filter(name=person)
    
    parties_1 = [(s.party, s.source.quote) for s in soirees]
    print(parties_1)

    parties = []
    for party, quote in parties_1:
        other_guests = Guest.objects.filter(party=party).exclude(name=qid).select_related("name")
        others = [ g.name.name for g in other_guests ]
        parties.append(
            {
                'party' : party,
                'quote' : quote,
                'others' : others,
            }
        )
    print(parties)

    template = loader.get_template("parties/person/specific.html")
    subj, poss = make_pronouns(person.gender)
    context= {
        'p' : person, 
        "have_detail" : True,
        "subj_pron" : subj,
        "poss_pron" : poss,
        "parties" : parties,
        }
    return HttpResponse(template.render(context, request))


def get_visdata_by_party(request):
    # party date, person
    all_parties = Party.objects.all()
    response = {
        'parties' : {},
    }
    for party in all_parties:
        print(party.year, party.month)
        response['parties'][party.pid] = {
                "year": party.year,
                "month": party.month if party.month else 6,
                "day": party.day if party.day else 1,
                "guests": [],
            }
    
    for mention in Guest.objects.all():
        response['parties'][mention.party.pid]['guests'].append(mention.name.qid)


    return JsonResponse(response)


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
            "ypos" : random.random()
        }
    
    for mention in Guest.objects.order_by("party"):
        response['people'][mention.name.qid]['parties'].append(
            {
                "year": mention.party.year,
                "month": mention.party.month if mention.party.month else 6,
                "day": mention.party.day if mention.party.day else 1,
            }
        )

    return JsonResponse(list(response["people"].values()), safe=False)
