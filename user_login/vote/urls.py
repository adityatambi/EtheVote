from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote, name="vote"),
    path('results', views.result, name= "result"),
    path('details', views.candidateDetails,name = "details")

]