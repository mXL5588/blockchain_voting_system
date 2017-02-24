from django.contrib import admin

# Register your models here.

from .models import Ballot, Choice


class BallotAdmin(admin.ModelAdmin):
   fieldsets = [
        (None,               {'fields': ['ballot_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

admin.site.register(Ballot, BallotAdmin)
admin.site.register(Choice)