'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question']}),
        (None, {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    
admin.site.register(Poll, PollAdmin)
