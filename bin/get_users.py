# How to run REPL scripts like this one:
# echo 'from bin import get_users' | pdm run python3 manage.py shell

from django.contrib.auth import get_user_model

print(
    "Superusers:\n",
    list(
        get_user_model()
        .objects.filter(is_superuser=True)
        .values_list("username", flat=True)
    ),
)

print(
    "Users:\n",
    list(
        get_user_model()
        .objects.filter(is_superuser=False)
        .values_list("username", flat=True)
    ),
)

# pdm run python3 manage.py changepassword <user>
