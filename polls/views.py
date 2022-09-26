from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Question


def index(request):
    last_five_questions = Question.objects.order_by("-date_published")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "last_five_questions": last_five_questions,
    }
    # output = "\n\n".join([q.asked_question for q in last_five_questions])
    return HttpResponse(template.render(context, request))


def details(request, question_id):
    try:
        target_question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    # Using render() from django.shortcuts as shorthand
    return render(request, "polls/details.html", {"question": target_question})


def results(request, question_id):
    target_question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": target_question})


def vote(request, question_id):
    return HttpResponse(f"Voting for question ${question_id}")
