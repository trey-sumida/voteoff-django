from django.contrib import admin
from .models import Contest, Choice, AllowedUsers, LastVote

admin.site.site_header = "VoteOff Admin"
admin.site.site_title = "VoteOff Admin Area"
admin.site.index_title = "Welcome to the VoteOff Admin Area"


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class ContestAdmin(admin.ModelAdmin):
    list_display = ('contest_title', 'creator', 'pub_date', 'start_date', 'end_date')
    readonly_fields = ('pub_date',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = [('Add Contest', {'fields': ['contest_title']}),
    ('Information', {'fields': ['public', 'creator', 'contest_description', 'contest_image', 'start_date', 'end_date']}),]
    inlines = [ChoiceInLine]


admin.site.register(LastVote)
admin.site.register(AllowedUsers)
admin.site.register(Contest, ContestAdmin)
