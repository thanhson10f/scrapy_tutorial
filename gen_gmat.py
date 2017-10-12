# encoding: utf-8
import codecs
import json

html = u''
question_list = []
with codecs.open('gmat.jl', 'rU', 'utf-8') as f:
    for line in f:
        question = json.loads(line)
        question_list.append(question)

question_list = sorted(question_list, key=lambda x: x['number'])
answer_list = u''

for question in question_list:
    temp = u'<div class="question">{0}. {1}'.format(question['number'], question['text'])
    temp = temp + '<ul>'
    for opt in question['options']:
        temp = temp + u'<li style="list-style: none">{0} - {1}</li>'.format(opt[0], opt[1])
    temp = temp + '</ul></div>'
    html = html + temp

    answer_list += u'{0}. {1}<br>'.format(question['number'], question['answer'])
with codecs.open('gmat.html', 'w', 'utf-8') as f:
    f.write(html)
with codecs.open('answer.html', 'w', 'utf-8') as f:
    f.write(answer_list)
