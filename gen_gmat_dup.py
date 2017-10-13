# -*- coding: utf8 -*-
import codecs
import json

html = u''
question_list = []
with codecs.open('gmatdup.jl', 'rU', 'utf-8') as f:
    for line in f:
        question = json.loads(line)
        question_list.append(question)

question_list = sorted(question_list, key=lambda x: (x['qid'], x['subid']))
answer_list = u''

old_qid = ''
current_num = 0
temp = ''
for question in question_list:
    qid = question['qid']
    if old_qid != qid:
        current_num += 1
        temp += u'<br><div class="question"><b>Essay {0}</b> ({1}). <strong>{2}</strong></div>'.format(current_num, question['qid'], question['text'])

    temp += u'<br><u>Question {0}:</u> <i>{1}</i>'.format(question['subid'], question['choice_question'])
    temp = temp + '<ul>'
    for opt in question['options']:
        temp = temp + u'<li style="list-style: none">{0} - {1}</li>'.format(opt[0], opt[1])
    temp = temp + '</ul>'

    if old_qid != qid:
        answer_list += u'<br><b>Essay {0}</b> ({1})<br>'.format(current_num, qid)

    answer_list += u'Question {0}: {1}<br>'.format(question['subid'], question['answer'])
    old_qid = qid

with codecs.open('gmatdup.html', 'w', 'utf-8') as f:
    f.write(temp)
with codecs.open('answerdup.html', 'w', 'utf-8') as f:
    f.write(answer_list)
