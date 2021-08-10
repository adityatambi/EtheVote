from django.shortcuts import render, get_object_or_404
from .models import Voter


# Create your views here.

def detail(request, id):
    # voter = Voter.objects.get(pk=id)
    voter = get_object_or_404(Voter, pk=id)
    return render(request, "voters/detail.html", {"voter": voter})


def list(request):
    return render(request, "voters/list.html",
                  {"voter": Voter.objects.all()})
