from django.db import models
from datetime import time
from django.core.exceptions import ValidationError
from django.db.models import Q, F
# Create your models here.
class Election_start_stop(models.Model):
    index= models.IntegerField(db_index=True, primary_key=True)
    Election_status = models.BooleanField()
    start_time= models.DateTimeField(blank= True)
    end_time= models.DateTimeField(blank= True)


    def __str__(self):
        return f"Current Status {self.Election_status}"