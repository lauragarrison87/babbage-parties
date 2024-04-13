from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def index(request):
    context = {'foobar' : 'HELLO 3!!!'}
    template = loader.get_template("parties/index.html")
    return HttpResponse(template.render(context, request))

