# How to run REPL scripts like this one:
# echo 'from bin import clear_recent_actions' | pdm run python3 manage.py shell

from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()
