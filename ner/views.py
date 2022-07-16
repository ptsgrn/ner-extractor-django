from lib2to3.pgen2.token import AT
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.html import escape, escapejs, strip_tags
from pythainlp.tag import NER
import re

# สนใจ: date, time, location, person, organization
ALL_ENTITY = [
  "DATE",
  "TIME",
  "LOCATION",
  "PERSON",
  "ORGANIZATION",
]

def index(request):
  pner = NER(engine='thainer')
  text = request.POST.get('text', '')
  text = strip_tags(text)
  # text = escape(escapejs(text))
  text = re.sub(r'\[[0-9]{1,}\]', '', text)
  ner = pner.tag(text, tag=True)
  output = ''
  highlight_ner = ner
  entry = []
  for entity in ALL_ENTITY:
    p = re.compile(f'<{entity}>(.+?)</{entity}>')
    try:
      result = p.findall(ner)
    except AttributeError:
      result = []
    for o in result:
      entry.append({
        'entity': entity.lower(),
        'value': o
      })
    highlight_ner = p.sub(string=highlight_ner, repl=fr'<span class="tag-{entity.lower()}" title="{entity}">\1</span>')
  for e in entry:
    output += f"""
      <tr class="entities entity-{e['entity']}">
        <th class="row-{e['entity']}">{e['entity']}</th>
        <td>{e['value']}</td>
      </tr>
    """
  context = {
    'title': 'Tagged',
    'message': 'Welcome to the NER app!',
    'action': '/tag/',
    'output': highlight_ner,
    'entities': output,
  }
  return render(request, 'ner/index.html', context)

def tag(request):
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
