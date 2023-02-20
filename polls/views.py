from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }    
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        template = loader.get_template('polls/detail.html')
        question = Question.objects.get(pk=question_id)
        context = {
            'question': question
        }
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return HttpResponse(template.render(context, request))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        template = loader.get_template('polls/detail.html')
        context = {
            'question': question,
            'error_message': "You did not select a choice."
        }
        return HttpResponse(template.render(request, context))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
