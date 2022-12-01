# How to run REPL scripts like this one:
# echo 'from bin import setup_test_env' | pdm run python3 manage.py shell

from django.test import Client
from django.test.utils import setup_test_environment
from django.urls import reverse

setup_test_environment()  # Install template renderer
client = Client()

response = client.get("/")
print(response.status_code)

response = client.get(reverse("polls:index"))
print(response.status_code)
print(response.content)
print(response.context["last_five_questions"])
