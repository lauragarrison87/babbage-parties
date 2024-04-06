from django.db import models

class Person(models.Model):
    qid = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    presumed = models.BooleanField(default=False)
    birth = models.DateField()
    death = models.DateField()



