from django.shortcuts import render
from django.http import HttpResponse
from voters.models import Voter


# Create your views here.
def welcome(request):
    return render(request, "website/welcome.html",
                  {"num_voters":Voter.objects.count()})
                  #{"voter":Voter.objects.all()})
