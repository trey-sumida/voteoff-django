from django.contrib import admin
from .models import Question, Choice

admin.site.site_header = "VoteOff Admin"
admin.site.site_title = "VoteOff Admin Area"
admin.site.index_title = "Welcome to the VoteOff Admin Area"


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [('Add Question', {'fields': ['question_text']}),
    ('Information', {'fields': ['public', 'creator']}),]
    inlines = [ChoiceInLine]

# admin.site.register(Question)
# admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
