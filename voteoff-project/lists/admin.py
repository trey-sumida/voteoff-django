from django.contrib import admin
from .models import Question, Choice, Friend, UserProfile

admin.site.site_header = "VoteOff Admin"
admin.site.site_title = "VoteOff Admin Area"
admin.site.index_title = "Welcome to the VoteOff Admin Area"


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [('Add Question', {'fields': ['question_text']}),
    ('Information', {'fields': ['public', 'creator', 'participants']}),]
    inlines = [ChoiceInLine]

class FriendAdmin(admin.ModelAdmin):
    fieldsets = [('Add Friend',{'fields': ['from_user', 'to_user', 'accepted']}),]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(UserProfile)
