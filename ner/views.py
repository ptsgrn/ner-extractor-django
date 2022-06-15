from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import escape, escapejs, strip_tags
from pythainlp.tag import NER
import re

ALL_ENTITY = [
  "DATE",
  "TIME",
  "EMAIL",
  "LEN",
  "LOCATION",
  "ORGANIZATION",
  "PERSON",
  "PHONE",
  "URL",
  "ZIP",
  "MONEY",
  "LAW",
]

def tag(request):
  pner = NER(engine='thainer')
  text = request.POST.get('text', '')
  text = strip_tags(text)
  # text = escape(escapejs(text))
  text = re.sub(r'\[[0-9]{1,}\]', '', text)
  ner = pner.tag(text, tag=True)
  output = ''
  highlight_ner = ner
  for entity in ALL_ENTITY:
    p = re.compile(f'<{entity}>(.+?)</{entity}>')
    try:
      result = p.findall(ner)
    except AttributeError:
      result = ''
    output += '<tr class="' + entity.lower() +'"><th>' + entity + '</th><td><span class=tag-'+ entity.lower() +'>' + f'</span>, <span class=tag-{entity.lower()}>'.join(result) + '</span></td></tr>'
    # highlight_ner = p.sub(f'<{entity}>(.+?)</{entity}>', f'<span class="{entity.lower()}">\1</span>', highlight_ner)
    highlight_ner = p.sub(string=highlight_ner, repl=fr'<span class="tag-{entity.lower()}" title="{entity}">\1</span>')
  context = {
    'title': 'Tagged',
    'message': 'Welcome to the NER app!',
    'action': '/tag/',
    'output': highlight_ner,
    'entities': output
  }
  return render(request, 'ner/index.html', context)


def index(request):
  pner = NER(engine='thainer')
  text = request.POST.get('text', '')
  text = strip_tags(text)
  # text = escape(escapejs(text))
  text = re.sub(r'\[[0-9]{1,}\]', '', text)
  ner = pner.tag(text)
  output = ''
  highlight_ner = ner
  context = {
    'title': 'NER',
    'message': 'Welcome to the NER app!',
    'action': '/',
    'output': highlight_ner,
    'entities': output
  }
  return render(request, 'ner/index.html', context)
