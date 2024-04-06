from django.db import models

class Person(models.Model):
    qid = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=False)
    presumed = models.BooleanField(default=False)
    birth = models.DateField(null=True)
    death = models.DateField(null=True)

    def __str__(self):
        return f'{self.name} (Q{self.qid})'


class Source(models.Model):
    sid = models.CharField("Source ID", max_length=80, primary_key=True)
    source = models.CharField(max_length=80, null=True)
    quote = models.TextField(null=False)
    pages = models.CharField(max_length=80, null=True)

    def __str__(self):
        return self.sid
