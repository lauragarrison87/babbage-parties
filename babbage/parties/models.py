from django.db import models

class Person(models.Model):
    qid = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    presumed = models.BooleanField(default=False)
    birth = models.DateField(null=True)
    death = models.DateField(null=True)

    def __str__(self):
        return f'{self.name} (Q{self.qid})'

