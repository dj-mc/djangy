from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question

# from django.http import Http404, HttpResponse, HttpResponseRedirect
# from django.template import loader

# Index view


# def index(request):
#     last_five_questions = Question.objects.order_by("-date_published")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "last_five_questions": last_five_questions,
#     }
#     return HttpResponse(template.render(context, request))


class IndexView(generic.ListView):
    # Override default question_detail.html template
    template_name = "polls/index.html"
    # Override default {{ question_list }} context variable
    context_object_name = "last_five_questions"

    def get_queryset(self):
        """
        Return the last five published questions, lte (<=) to timezone.now().
        Exclude questions which have a future date_published attribute.
        """
        return Question.objects.filter(date_published__lte=timezone.now()).order_by(
            "-date_published"
        )[:5]


# Details view

# def details(request, question_id):
#     try:
#         target_question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     # Using render() from django.shortcuts as shorthand
#     return render(request, "polls/details.html", {"question": target_question})


class DetailsView(generic.DetailView):  # Expects pk value from urls.py
    # Generic views need to know their model
    model = Question
    template_name = "polls/details.html"


# Results view

# def results(request, question_id):
#     target_question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": target_question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# Voting view


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
