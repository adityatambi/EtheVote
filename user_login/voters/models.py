from django.db import models


# Create your models here.


class Voter(models.Model):
    index = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=10, primary_key=True)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(blank=True, max_length=6)

    def save(self):
        self.index = Voter.objects.count()
        super(Voter, self).save()
    def __str__(self):
        return f"{self.name}. {self.user}."
