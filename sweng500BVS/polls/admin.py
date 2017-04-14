from django.contrib import admin
from .models import Ballot, VoterChoice, ContestantChoice, VotersList, VotersListChoice
import json
import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from .counterparty import *








class VoterChoiceInline(admin.TabularInline):
    model = VoterChoice
    extra = 3

class ContestantChoiceInline(admin.TabularInline):
    model = ContestantChoice
    extra = 3


class BallotAdmin(admin.ModelAdmin):
    ballotAddress = ""
    fieldsets = [
        (None,               {'fields': ['ballot_name']}),
        (None,               {'fields': ['ballot_address']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['expand']}),
        ('Date information', {'fields': ['end_date'], 'classes': ['expand']}),
    ]
    #inlines = []
    inlines = [ContestantChoiceInline,VoterChoiceInline]
    
    # include a list filter
    list_filter = ['pub_date']
    list_display = ('ballot_name', 'ballot_address', 'pub_date', 'end_date', 'was_published_recently')

	
    # include a ballot search
    search_fields = ['ballot_name']

    def save_model(self, request, obj, form, change):
        print("********************************************************************************")
        print("Issuance: ", obj.ballot_address)
        if obj.ballot_issued == False:
          #input code to check XCP balance here then execute burnBTC if the amount is less than .5 XCP
          #burnBTC(sourceAddress, AmountInSatoshisToBurn)

          #validate a bitcoin address
          validCheck = validateAddress(obj.ballot_address)

          response = createIssuance(obj.ballot_address,obj.ballot_name)
          jsonObj = json.loads(response.text)
          if 'error' not in jsonObj:
            print("Response 1: ", jsonObj)
            response = signRawTransaction(jsonObj['result'])
            #unconfirmedAssetBalance = getUnconfirmedQuantity(getXCPTxInfo(jsonObj['result']))
            jsonObj = json.loads(response.text)
            if 'error' in jsonObj:
              print("Response 2: ", jsonObj)
              response = sendRawTransaction(jsonObj['result']['hex'])
              jsonObj = json.loads(response.text)
              if 'error' in jsonObj:
                print("Response 3: ", jsonObj)
                obj.ballot_issued = True
              else:
                print("Error-3 Response: ", jsonObj)
            else:
              print("Error-2 Response: ", jsonObj)
          else:
            print("Error-1 Response: ", jsonObj)
        super().save_model(request, obj, form, change)
    




        
    def save_formset(self, request, form, formset, change):
      print("___________________________________________________________________________________")
      # Create instances. Each instance will be a "row" (obj) of the inline model
      instances = formset.save(commit=False)
      if form.instance.isItVoter == True:
        # Iterate over the instances (objects of the Inline Model)
        for instance in instances:
            # Get the object's attribute (Model field)
            print("Voter Address: ", instance.voter_address)
            print("Voter Text: ", instance.voter_name)
            
            #validate a bitcoin address
            validCheck = validateAddress(instance.voter_address)
            #send fee amount to voter for resend to candidate
            sendBTCToAddress(instance.voter_address, .01)
            response = createSend(form.instance.ballot_address, instance.voter_address, form.instance.ballot_name)
            jsonObj = json.loads(response.text)
            if 'error' not in jsonObj:
              print("Response 1: ", jsonObj)
              response = signRawTransaction(jsonObj['result'])
              unconfirmedAssetBalance = getUnconfirmedQuantity(getXCPTxInfo(jsonObj['result']))
              jsonObj = json.loads(response.text)
              if 'error' in jsonObj:
                print("Response 2: ", jsonObj)
                response = sendRawTransaction(jsonObj['result']['hex'])
                jsonObj = json.loads(response.text)
                if 'error' in jsonObj:
                  print("Response 3: ", jsonObj)
                  print("Unconfirmed Balance for: ", instance.voter_name, ":", unconfirmedAssetBalance)
                  print("Confirmed Balance for: ", instance.voter_name, ":", getBalance(instance.voter_address, form.instance.ballot_name))
                else:
                  print("Error-3 Response: ", jsonObj)
              else:
                print("Error-2 Response: ", jsonObj)
            else:
              print("Error-1 Response: ", jsonObj)
        form.instance.isItVoter = False
      else:
        form.instance.isItVoter = True


      print("Balance for ", form.instance.ballot_name, ":", getBalance(form.instance.ballot_address, form.instance.ballot_name))
      super().save_formset(request,form, formset, change)

admin.site.register(Ballot, BallotAdmin)


class VotersListChoiceInline(admin.TabularInline):
    model = VotersListChoice
    extra = 3

class VotersListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['votersList_name']}),
        (None,               {'fields': ['currentVoterChoice']}),
    ]
    #inlines = []
    inlines = [VotersListChoiceInline]
    

    # include a ballot search
    search_fields = ['votersList_name']


admin.site.register(VotersList, VotersListAdmin)