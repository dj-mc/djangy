# How to run REPL scripts like this one:
# echo 'import playground' | pdm run python3 manage.py shell

from django.contrib.auth import get_user_model
list(get_user_model().objects.filter(is_superuser=True).values_list('username', flat=True))

# pdm run python3 manage.py changepassword <user>
