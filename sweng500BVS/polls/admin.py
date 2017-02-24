from django.contrib import admin
from .models import Ballot, Choice
# Register your models here.



class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class BallotAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['ballot_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    
    # include a list filter
    list_filter = ['pub_date']
    list_display = ('ballot_text', 'pub_date', 'was_published_recently')
	
    # include a ballot search
    search_fields = ['ballot_text']

admin.site.register(Ballot, BallotAdmin)