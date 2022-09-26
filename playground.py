# How to run REPL scripts like this one:
# echo 'import playground' | pmd run python3 manage.py shell
from django.utils import timezone
from polls.models import Question


def all_questions():
    return Question.objects.all()


def pprint_vars(obj):
    from pprint import pprint

    pprint(vars(obj))


def print_all_attributes(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def print_Q_attr(Q):
    print(Q.id, Q.asked_question, Q.date_published)


def ask_a_question(question):
    # Expects a datetime with tzinfo for date_published,
    # so use timezone.now() instead of datetime.datetime.now().
    new_Q = Question(asked_question=question, date_published=timezone.now())
    new_Q.save()
    print_Q_attr(new_Q)
    return new_Q


print(all_questions()[0])
pprint_vars(all_questions()[0])


# AttributeError: Manager isn't accessible via Question instances
# print_all_attributes(all_questions()[0])


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

# # Make sure our custom method worked.
# q = Question.objects.get(pk=1)
# q.was_recently_published()

# # Construct new Choice objects
# q.choice_set.create(question_choice="Not much", votes=0)
# q.choice_set.create(question_choice="The sky", votes=0)
# c = q.choice_set.create(question_choice="Just hacking again", votes=0)

# c.question  # Choice objects relate to Question objects
# q.choice_set.all()  # Same thing
# q.choice_set.count()

# # Double underscores separate relationships recursively
# # Find all Choices for any question whose date_published is in this year
# Choice.objects.filter(question__date_published__year=current_year)

# # Filter then delete
# c = q.choice_set.filter(question_choice__startswith="Just hacking")
# c.delete()
