from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse

from .models import Choice, Question


def index(request):
    last_five_questions = Question.objects.order_by("-date_published")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "last_five_questions": last_five_questions,
    }
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
    target_question = get_object_or_404(Question, pk=question_id)
    try:
        # Use request.POST["choice"] because voting will alter data
        selected_choice = target_question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):  # Go back to form and try again
        return render(
            request,
            "polls/details.html",
            {"question": target_question, "error_message": "No choice selected"},
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Redirect to prevent double posting if a user hits back
        return HttpResponseRedirect(
            reverse("polls:results", args=(target_question.id,))
        )
