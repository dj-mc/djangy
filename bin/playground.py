# How to run REPL scripts like this one:
# echo 'from bin import playground' | pdm run python3 manage.py shell

import datetime
from django.utils import timezone
from polls.models import Question


def all_questions():
    return Question.objects.all()


def pprint_vars(obj):
    from pprint import pprint

    pprint(vars(obj))


def print_all_attributes(obj):
    for attr in dir(obj):
        print(f"obj.${attr} = ${getattr(obj, attr)}")


def print_Q_attr(Q):
    print(f"id: ${Q.id}", f"Q: {Q.asked_question}", f"date: ${Q.date_published}")


def ask_a_question(question):
    # Expects a datetime with tzinfo for date_published,
    # so use timezone.now() instead of datetime.datetime.now().
    new_Q = Question(asked_question=question, date_published=timezone.now())
    new_Q.save()
    print_Q_attr(new_Q)
    return new_Q


def create_choices(question, choices_list):
    for choice in choices_list:
        question.choice_set.create(question_choice=choice, votes=0)
    print("Choices:", question.choice_set.all())
    print("Number of choices:", question.choice_set.count())


# 30 days in the future
future_question = Question(date_published=timezone.now() + datetime.timedelta(days=30))
print(future_question.was_recently_published())  # Should expose a bug

# sleep_Q = ask_a_question("How many hours of sleep do you get per night?")
# create_choices(sleep_Q, [6, 7, 8, 9, 10])

# AttributeError: Manager isn't accessible via Question instances
# print_all_attributes(all_questions()[0])

# pprint_vars(all_questions())

print(all_questions())

# # Mutate attributes then save
# q.asked_question = "Why do you program in Python?"
# q.save()

# # Lookup API with keyword arguments
# Question.objects.filter(id=1)
# Question.objects.filter(asked_question__startswith="Why")

# current_year = timezone.now().year
# Question.objects.get(date_published__year=current_year)

# # Wrong id will raise an exception
# Question.objects.get(id=999)

# # Lookup by primary key
# Question.objects.get(pk=1)
# # (pk=1 is e.q. to id=1)
# q = Question.objects.get(pk=1)
# q.was_recently_published()

# # Double underscores separate relationships recursively
# # Find all Choices for any question whose date_published is in this year
# Choice.objects.filter(question__date_published__year=current_year)

# # Filter then delete
# c = q.choice_set.filter(question_choice__startswith="Just hacking")
# c.delete()
