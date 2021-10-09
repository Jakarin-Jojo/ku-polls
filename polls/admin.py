"""System management in the admin section."""
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Setting a default Choice Online is 3 choices."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Register Question model in the Admin page."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', 'is_published', 'can_vote')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
