# Register models

from django.contrib import admin
from .models import Choice, Question


# Or admin.StackedInline
class InlineChoices(admin.TabularInline):
    # Display 3 inline extra choice slots
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # Objects are displayed as str() by default
    # instead use list_display to display specifics:
    list_display = ("asked_question", "date_published", "was_recently_published")
    list_filter = ["date_published"]  # Filter questions by date_published

    # Search functionality uses a LIKE query on database
    search_fields = ["asked_question"]  # Search for a question

    # Customize how data fields are displayed
    fieldsets = [
        (None, {"fields": ["asked_question"]}),
        ("Metadata", {"fields": ["date_published"]}),
    ]
    inlines = [InlineChoices]


# Register Question as its own page
# Also display 3 inline extra choice slots
admin.site.register(Question, QuestionAdmin)
# Also register Choice as its own (optional) page
admin.site.register(Choice)
